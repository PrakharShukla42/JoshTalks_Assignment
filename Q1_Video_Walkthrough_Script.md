# Video Walkthrough Script (Target: 1.5 - 2 Minutes)

**(0:00 - 0:15) Introduction & The Eval Choice**
"Hi, I'm [Your Name], and for this challenge, I designed the 'Bharat-Realism' text-to-image eval. The goal here is simple: Can AI models generate culturally accurate, relatable lifestyle images of Indian clothing in everyday, non-glamorous settings? I chose this because in Indian e-commerce, relatable local contexts convert way better than hyper-glamorous stereotypes."

**(0:15 - 0:45) The Setup**
"I evaluated OpenAI’s GPT Image 1, Gemini 2.5 Flash, and the new Gemini 3.1 Flash. I used a highly specific prompt for a 25-year-old Indian man wearing an olive green kurta on a middle-class Mumbai balcony in the evening. I then asked 10 participants to blindly rate the outputs on Cultural Authenticity, Realism, and Prompt Adherence via a custom React rating UI, which I’ve built in my submission."

**(0:45 - 1:15) The Findings**
"Here is what I found: Models really struggle with 'ordinary'. GPT Image 1 followed the prompt perfectly but the images looked like an expensive, hyper-saturated studio ad—missing the 'candid smartphone' requirement completely. Gemini 3.1 Flash was the clear winner for Realism; it actually captured the gritty, natural lighting of a phone camera and accurate architectural details like standard Indian window grills."

**(1:15 - 1:50) Why It Matters & Future Scope**
"Why does this matter to an AI lab building for India? Because 'good enough for global' is not 'accurate enough for local'. The ability to generate this 'Bharat Realism' without hallucinating stereotypes is exactly what enterprise clients are willing to pay for. 

Looking to the future, we wouldn't just rely on human raters. As part of my submission, I've designed an automated pipeline where we treat a Vision-Language Model like a specialized GPT: you simply feed it the prompt and the generated image, and it acts as an automated judge to rate them instantly. Thank you for watching!"
