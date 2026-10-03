import pandas as pd

def flag_suspicious_tasks(df):
    """
    Applies the 3 rules designed in Question 2 to flag suspicious transcriptions.
    """
    # Initialize strike column
    df['strike_reason'] = None
    
    # Trigger 1: Speed-Limit Violation (Bot/Copy-Paste)
    trigger1_mask = df['segment_character_per_second'] > 15
    df.loc[trigger1_mask, 'strike_reason'] = "Trigger 1: Impossible Typing Speed (>15 CPS)"
    
    # Trigger 2: The Impossible Review (Blind Accept)
    # They spent less than 75% of the audio duration and didn't edit. (Ignore clips under 3s)
    trigger2_mask = (df['time_taken_by_user'] < (df['duration'] * 0.75)) & (df['is_edited'] == False) & (df['duration'] > 3.0)
    # Don't overwrite trigger 1 if it already exists
    df.loc[trigger2_mask & df['strike_reason'].isnull(), 'strike_reason'] = "Trigger 2: Blind Accept (Time < 75% Duration)"
    
    # Trigger 3: The Impossible Edit
    # They edited the text but spent less than 40% of the audio duration. (Ignore clips under 5s)
    trigger3_mask = (df['time_taken_by_user'] < (df['duration'] * 0.40)) & (df['is_edited'] == True) & (df['duration'] > 5.0)
    df.loc[trigger3_mask & df['strike_reason'].isnull(), 'strike_reason'] = "Trigger 3: Impossible Edit (Time < 40% Duration)"
    
    # Create a boolean column for easy counting
    df['has_strike'] = df['strike_reason'].notnull()
    return df

def analyze_users(df):
    """
    Applies the Rolling Strike System to block users who accumulate 3 strikes.
    """
    print("--- Transcriber Quality Report ---")
    
    # Group by user to check strike counts
    # In a real system, this would be a rolling window of the last 10 tasks.
    # For this simulation, we'll check total strikes in the dataset.
    
    user_stats = df.groupby('user_id').agg(
        total_tasks=('task_id', 'count'),
        total_strikes=('has_strike', 'sum')
    ).reset_index()
    
    for _, row in user_stats.iterrows():
        user = row['user_id']
        strikes = row['total_strikes']
        total = row['total_tasks']
        
        print(f"\nUser: {user} | Tasks: {total} | Strikes: {strikes}")
        
        if strikes >= 3:
            print("  [ACTION] ACCOUNT SUSPENDED: Accumulated 3 or more strikes.")
            print("  [ACTION] Flagged previous tasks for Internal QA Review.")
            # Print the specific strikes for this user
            user_tasks = df[(df['user_id'] == user) & (df['has_strike'] == True)]
            for _, task in user_tasks.iterrows():
                print(f"    - Task {task['task_id']}: {task['strike_reason']}")
        elif strikes > 0:
            print("  [WARNING] User has strikes, but under threshold for suspension.")
        else:
            print("  [STATUS] Good Standing.")

if __name__ == "__main__":
    print("Loading data from sample_data.csv...")
    df = pd.read_csv("sample_data.csv")
    
    print("Flagging suspicious tasks...")
    processed_df = flag_suspicious_tasks(df)
    
    print("Analyzing user behavior...\n")
    analyze_users(processed_df)
    
    processed_df.to_csv("audited_data.csv", index=False)
    print("\nDetailed audit saved to 'audited_data.csv'.")
