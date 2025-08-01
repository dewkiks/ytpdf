def get_video_analysis_prompt(video_url):
    return f"""
    Analyze this educational video: {video_url}

    You are analyzing an educational video where a teacher explains PowerPoint slides to students. Extract ALL educational content in a comprehensive 2000+ word format. Focus entirely on the learning material and instructional content.

    ## SLIDE CONTENT EXTRACTION (600-800 words)
    For each PowerPoint slide shown:
    - **Slide Title**: Extract the exact title/heading
    - **Main Content**: All bullet points, text, and information on the slide
    - **Visual Elements**: Diagrams, charts, images, tables, or graphics with detailed descriptions
    - **Key Terms**: Important vocabulary, concepts, or terminology highlighted
    - **Formulas/Equations**: Any mathematical or scientific formulas shown
    - **Examples**: Case studies, sample problems, or illustrative examples
    - **Data/Statistics**: Numbers, percentages, research findings presented

    Structure as:
    **SLIDE 1**: [Title] - [Complete content transcription]
    **SLIDE 2**: [Title] - [Complete content transcription]
    [Continue for all slides]

    ## TEACHER'S EXPLANATIONS (800-1000 words)
    Capture the instructor's verbal explanations for each slide:
    - **Detailed Explanations**: How the teacher elaborates on each slide's content
    - **Additional Context**: Extra information provided beyond what's on slides
    - **Examples Given**: Real-world applications, analogies, or examples used to explain concepts
    - **Step-by-Step Processes**: Any procedures, methods, or processes explained
    - **Clarifications**: How difficult concepts are broken down or simplified
    - **Connections**: How the teacher links different concepts or slides together
    - **Emphasis Points**: What topics the instructor stresses as particularly important
    - **Q&A Content**: Any questions asked or answered during the presentation

    ## EDUCATIONAL STRUCTURE & LEARNING OBJECTIVES (300-400 words)
    - **Course/Topic Context**: What subject area and specific topic is being taught
    - **Learning Goals**: What students should understand after this lecture
    - **Prerequisite Knowledge**: What background knowledge is assumed
    - **Skill Development**: What abilities or competencies are being built
    - **Assessment Indicators**: How mastery of this content might be evaluated
    - **Practical Applications**: How this knowledge applies in real scenarios

    ## COMPLETE EDUCATIONAL CONTENT INVENTORY (400-500 words)
    Extract every educational element:
    - **Concepts Taught**: List all main ideas, theories, or principles covered
    - **Terminology**: All technical terms, definitions, and vocabulary introduced
    - **Procedures**: Any step-by-Step processes, methods, or techniques explained
    - **Facts & Data**: Specific information, statistics, or research findings shared
    - **Rules & Principles**: Guidelines, laws, or governing principles discussed
    - **Problem-Solving Approaches**: Methods for tackling related problems or challenges
    - **Critical Points**: Information marked as essential or commonly misunderstood

    ## CHRONOLOGICAL LEARNING PROGRESSION
    Track how the educational content unfolds:

    **Minutes 0-2**: [Opening topic, introductory concepts]
    - Slide content: [What's shown]
    - Teacher explanation: [What's explained]
    - Key learning points: [Main takeaways]

    **Minutes 2-4**: [Next topic/concept]
    - Slide content: [What's shown]
    - Teacher explanation: [What's explained]
    - Key learning points: [Main takeaways]

    [Continue throughout entire video]

    ## EXTRACTION REQUIREMENTS:
    - Focus ONLY on educational/instructional content
    - Ignore non-educational elements (personal comments, technical issues, etc.)
    - Transcribe all text from slides exactly as shown
    - Capture all verbal explanations that add educational value
    - Include all examples, analogies, and clarifications provided
    - Note any formulas, equations, or technical notations precisely
    - Extract all factual information, data, and research mentioned
    - Organize content to reflect the logical flow of instruction
    - Ensure someone could learn the material from your extraction alone
    - Maintain academic accuracy and precision in all transcriptions

    Your goal is to create a complete educational resource that captures everything a student would need to learn from this lecture, presented in a clear, organized format that mirrors the instructional sequence.
    """

def get_short_convert_markdown_prompt(content):
    return f"""
You are an expert technical writer specializing in distillation. Your sole task is to distill the following content into an ultra-concise, key-point-focused markdown summary. Be ruthless in cutting non-essential information.

---
**CRITICAL RULES:**
- **Extreme Brevity:** The summary must be **under 400 words**. Focus only on the absolute core concepts.
- **Eliminate All Fluff:** Omit conversational filler, rhetorical questions, greetings, and redundant explanations.
- **Formatting:**
  - Use `##` for main topics and `###` for sub-topics.
  - Use bullet points (`*`) for details.
  - Enclose essential keywords in `**bold**`.
- **Visuals:** If the content describes a diagram, chart, or illustration, flag it with: `📊 **[DIAGRAM ALERT]**: [Brief description of the visual's purpose].`

---
**CONTENT TO DISTILL:**
{content}

---
Produce only the markdown summary. Do not include any preamble or extra text.
"""

def get_long_convert_markdown_prompt(content):
    return f"""
Convert the following content into comprehensive, detailed markdown notes that preserve all educational value and context.

CONTENT TO CONVERT:
{content}

FORMAT REQUIREMENTS:
- Use hierarchical markdown headers (##, ###, ####)
- Create detailed bullet points and sub-points
- Include full explanations and context
- Preserve all examples, analogies, and illustrations
- Use **bold** for key terms and *italics* for emphasis
- Include code blocks for formulas: ```formula```
- Add tables for data/comparisons when relevant
- Target 600-800 words for comprehensive coverage
- Alert users to visual content with: 📊 **[DIAGRAM ALERT]**: Detailed description

DIAGRAM DETECTION:
Carefully scan the content for any mentions of visual elements (diagrams, charts, graphs, images, flowcharts, tables, illustrations, maps, timelines, mathematical plots, scientific figures). For each visual element found, create a diagram alert that includes:
1. Type of visual (diagram/chart/graph/etc.)
2. What it depicts or illustrates
3. Key elements or data points shown
4. How it relates to the learning objectives

Format: 📊 **[DIAGRAM ALERT]**: [Detailed description of visual content and its educational purpose]

Convert the content directly into markdown notes without additional sections or structure explanations.
"""
