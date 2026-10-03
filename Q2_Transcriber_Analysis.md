# Question 2: Transcriber Quality Analysis

## Part I: Identifying Warning Signs

### Warning Sign 1: The "Blind Accept" (Rushing without listening)
* **What it tells us:** The transcriber is simply accepting the AI (Whisper) output as perfect without actually listening to the audio, attempting to maximize their payout by churning through tasks quickly.
* **How to measure it:** Compare the `time_taken_by_user` against the audio `duration` when `is_edited` is False. To verify a transcription is 100% correct, a human must listen to the audio at normal speed.
* **Red flag thresholds:** If `time_taken_by_user` < (`duration` * 0.75) AND `is_edited` == False. (e.g., They spent 4 seconds "verifying" a 10-second audio clip).
* **False alarms:** Very short audio clips (under 2-3 seconds) where the human might comprehend the single word instantly, or if the user plays the audio at 1.5x or 2x speed (if the platform allows speed controls).

### Warning Sign 2: The "Bot / Copy-Paste Abuser"
* **What it tells us:** The transcriber knows the system checks if they made an edit, so they are either pasting pre-written text, pasting gibberish, or using an automated script to replace the text instantly.
* **How to measure it:** Look at the `segment_character_per_second` metric. Professional human typing speed rarely exceeds 6-8 characters per second (approx. 70-95 WPM).
* **Red flag thresholds:** If `segment_character_per_second` > 12. This physically impossible typing speed strongly indicates the user just copy-pasted text to bypass the `is_edited` check.
* **False alarms:** The user might be using browser text-expansion shortcuts (e.g., typing "/inaud" expands to "[inaudible background noise]") which artificially spikes the character count in a single second.

### Warning Sign 3: The "Impossible Edit"
* **What it tells us:** The transcriber submitted a modified text (`is_edited` = True), but spent so little time on the task that they couldn't possibly have listened to the audio *and* typed the correction.
* **How to measure it:** Check if `is_edited` is True but `time_taken_by_user` is significantly less than the audio `duration`. 
* **Red flag thresholds:** If `is_edited` == True AND `time_taken_by_user` < (`duration` * 0.4). For instance, fixing a transcript for a 15-second audio in just 5 seconds means they guessed the correction without listening to the whole clip.
* **False alarms:** The Whisper error was in the first 2 seconds of the audio, and the rest was silent or perfectly correct, allowing the user to fix it and submit early.

---

## Part II: Automated System Recommendations for Engineering

To automatically spot and block problematic transcribers without accidentally banning good users for occasional anomalies, I recommend implementing a **"Rolling Strike System"** rather than blocking based on a single task.

**To the Engineering Team:**
Please implement the following three real-time triggers on the backend evaluation pipeline.

**Trigger 1: Speed-Limit Violation**
```text
IF segment_character_per_second > 15:
    Log 1 STRIKE for User
```

**Trigger 2: The Impossible Review**
```text
IF (time_taken_by_user < duration * 0.75) AND (is_edited == FALSE) AND (duration > 3.0 seconds):
    Log 1 STRIKE for User
```
*(Note: We ignore clips under 3 seconds to avoid false alarms).*

**Trigger 3: The Impossible Edit**
```text
IF (time_taken_by_user < duration * 0.4) AND (is_edited == TRUE) AND (duration > 5.0 seconds):
    Log 1 STRIKE for User
```

**Action Engine (Account Blocking Logic):**
We do not block on a single strike, as humans make mistakes or find workarounds (like 2x audio speed). We block on a pattern of bad behavior.

```text
IF User accumulates 3 STRIKES within a rolling window of their last 10 completed tasks:
    1. SUSPEND User account (Block from accepting new tasks).
    2. Flag User's previous 50 submitted tasks with status = "Requires Internal QA Review".
    3. Withhold pending payout until Internal QA clears the flagged tasks.
```

**Why this works for the Transcriber Experience:** 
By using a rolling window (3 strikes out of 10), good transcribers who legitimately speed through a few easy tasks won't be penalized. Only users systematically abusing the platform will hit the threshold.
