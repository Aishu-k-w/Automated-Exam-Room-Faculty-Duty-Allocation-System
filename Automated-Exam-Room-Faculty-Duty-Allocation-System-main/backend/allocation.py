import pandas as pd
import re

def extract_usn_parts(usn):
    """Extract prefix and numeric part from USN."""
    match = re.match(r'^(.*?)(\d+)$', usn)
    if match:
        prefix, number = match.groups()
        return prefix, int(number)
    raise ValueError("Invalid USN format")

def generate_next_usn(current_usn, increment=1):
    """Generate next USN by incrementing the numeric part."""
    prefix, numeric_part = extract_usn_parts(current_usn)
    return f"{prefix}{numeric_part + increment:03d}"

def allocate_students_to_classrooms(num_students, start_usn, classroom_file):
    """
    Allocate students to classrooms based on capacity.
    
    Args:
        num_students (int): Total number of students to allocate
        start_usn (str): Starting USN (e.g., '1MS20CS001')
        classroom_file (str): Path to Excel file with columns: Classroom, Capacity
    
    Returns:
        pandas.DataFrame: Allocation results with columns:
            Classroom, Starting USN, Ending USN, Total Students
    """
    try:
        # Read classroom data
        df = pd.read_excel(classroom_file)
        if not all(col in df.columns for col in ['Classroom', 'Capacity']):
            raise ValueError("Excel file must contain 'Classroom' and 'Capacity' columns")
        
        # Sort classrooms by capacity (descending)
        df = df.sort_values('Capacity', ascending=False)
        
        # Initialize allocation results
        allocation_results = []
        remaining_students = num_students
        current_usn = start_usn
        
        # Allocate students to classrooms
        for _, row in df.iterrows():
            if remaining_students <= 0:
                break
                
            classroom = row['Classroom']
            capacity = row['Capacity']
            
            # Calculate students for this classroom
            students_in_room = min(capacity, remaining_students)
            
            # Calculate ending USN
            ending_usn = generate_next_usn(current_usn, students_in_room - 1)
            
            # Add to results
            allocation_results.append({
                'Classroom': classroom,
                'Starting USN': current_usn,
                'Ending USN': ending_usn,
                'Total Students': students_in_room
            })
            
            # Update for next iteration
            remaining_students -= students_in_room
            current_usn = generate_next_usn(ending_usn, 1)
        
        # Create result DataFrame
        result_df = pd.DataFrame(allocation_results)
        
        # Add summary row if there are remaining students
        if remaining_students > 0:
            result_df = pd.concat([result_df, pd.DataFrame([{
                'Classroom': 'Unallocated',
                'Starting USN': current_usn,
                'Ending USN': generate_next_usn(current_usn, remaining_students - 1),
                'Total Students': remaining_students
            }])], ignore_index=True)
        
        return result_df
        
    except Exception as e:
        raise Exception(f"Error in allocation: {str(e)}")

def parse_time_range(time_str):
    """Parse a time range string like '09:30-11:00' or '10:00-11:00' into (start_min, end_min)."""
    try:
        start, end = time_str.split('-')
        start_h, start_m = map(int, start.strip().split(':'))
        end_h, end_m = map(int, end.strip().split(':'))
        return start_h * 60 + start_m, end_h * 60 + end_m
    except Exception:
        return None, None

def is_time_overlap(t1, t2):
    """Check if two time ranges (start1, end1) and (start2, end2) overlap."""
    s1, e1 = parse_time_range(t1)
    s2, e2 = parse_time_range(t2)
    if None in (s1, e1, s2, e2):
        return False  # If parsing fails, assume no overlap
    return max(s1, s2) < min(e1, e2)

def allocate_faculty_to_classrooms(classroom_allocation_file, exam_timetable_file, faculty_timetable_file):
    """
    Allocate faculty to classrooms for each exam slot, following constraints.
    Args:
        classroom_allocation_file (str): Path to Excel with classroom allocations
        exam_timetable_file (str): Path to Excel with exam timetable
        faculty_timetable_file (str): Path to Excel with faculty regular timetable
    Returns:
        pandas.DataFrame: Allocation results with columns:
            Date, Day, Time, Subject, Classroom, Faculty
    """
    try:
        # Read input files
        class_df = pd.read_excel(classroom_allocation_file)
        exam_df = pd.read_excel(exam_timetable_file)
        faculty_df = pd.read_excel(faculty_timetable_file)

        # Clean up columns
        class_df = class_df[class_df['Classroom'] != 'Unallocated']
        class_list = class_df['Classroom'].tolist()
        # Use 'Faculty' column from faculty timetable
        faculty_list = faculty_df['Faculty'].unique().tolist()

        # Build faculty busy slots: {(Faculty, Day): [(Time, ...)]}
        busy_slots = {}
        for _, row in faculty_df.iterrows():
            key = (row['Faculty'], str(row['Day']).strip())
            busy_slots.setdefault(key, []).append(str(row['Time']).strip())

        # Track faculty allocations
        faculty_allocation_count = {f: 0 for f in faculty_list}
        faculty_slot_assigned = set()  # (Faculty, Date, Time)

        allocation_results = []

        for _, exam in exam_df.iterrows():
            date = exam['Date']
            day = str(exam['Day']).strip()
            time = str(exam['Time']).strip()
            subject = exam['Subject']
            used_faculty_this_slot = set()
            for classroom in class_list:
                # Find available faculty
                available = []
                for f in faculty_list:
                    # Check for time overlap with any busy slot
                    busy_times = busy_slots.get((f, day), [])
                    has_overlap = any(is_time_overlap(time, busy_time) for busy_time in busy_times)
                    if has_overlap:
                        continue
                    if faculty_allocation_count[f] >= 3:
                        continue
                    if (f, date, time) in faculty_slot_assigned:
                        continue
                    if f in used_faculty_this_slot:
                        continue
                    available.append(f)
                if not available:
                    faculty = 'Not Assigned'
                else:
                    faculty = available[0]
                    faculty_allocation_count[faculty] += 1
                    faculty_slot_assigned.add((faculty, date, time))
                    used_faculty_this_slot.add(faculty)
                allocation_results.append({
                    'Date': date,
                    'Day': day,
                    'Time': time,
                    'Subject': subject,
                    'Classroom': classroom,
                    'Faculty': faculty
                })

        result_df = pd.DataFrame(allocation_results)
        
        # Format the Date column as DD-MM-YYYY
        result_df['Date'] = pd.to_datetime(result_df['Date']).dt.strftime('%d-%m-%Y')
        
        return result_df
    except Exception as e:
        raise Exception(f"Error in faculty allocation: {str(e)}") 