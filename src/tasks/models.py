import json
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator

class TaskSubmission(BaseModel):
    """
    Model for handling task submissions for LLM story and educational content generation.

    Fields:
        prompt: Initial prompt for the LLM.
        technology: Technology used (Gemini, ChatGPT, etc.).
        story: Generated story/response from the LLM.

        theme_prompt: Theme transformation prompt.
        theme_placeholders: Placeholders for theme transformation.
        theme_story: Theme transformation result.
        theme_original_story: Original story before theme transformation.

        education_prompt: Educational enhancement prompt.
        education_placeholders: Placeholders for education prompt.
        education_story: Modified story after education prompt.
        education_original_story: Original story before educational enhancement.

        questions_prompt: Question generation prompt.
        questions_placeholders: Placeholders for questions/responses prompt.
        questions: Generated questions.
        questions_original_story: Original story for question generation.
    """
    prompt: str = Field("", description="Initial prompt for the LLM")
    technology: str = Field("", description="Technology used (Gemini, ChatGPT, etc.)")
    story: str = Field("", description="Generated story/response from the LLM")

    theme_prompt: Optional[str] = Field(None, description="Theme transformation prompt")
    theme_placeholders: Optional[str] = Field(None, description="Placeholders for theme transformation")
    theme_story: Optional[str] = Field(None, description="Theme transformation result")
    theme_original_story: Optional[str] = Field(None, description="Original story before theme transformation")

    education_prompt: Optional[str] = Field(None, description="Educational enhancement prompt")
    education_placeholders: Optional[str] = Field(None, description="Placeholders for education prompt")
    education_story: Optional[str] = Field(None, description="Modified story after education prompt")
    education_original_story: Optional[str] = Field(None, description="Original story before educational enhancement")

    questions_prompt: Optional[str] = Field(None, description="Question generation prompt")
    questions_placeholders: Optional[str] = Field(None, description="Placeholders for questions/responses prompt")
    questions: Optional[str] = Field(None, description="Generated questions")
    questions_original_story: Optional[str] = Field(None, description="Original story for question generation")

    @field_validator('prompt')
    def validate_prompt(cls, v: str) -> str:
        v = v.strip()
        if len(v) > 5000:
            raise ValueError("LLM prompts cannot exceed 5000 characters. Please shorten your prompt.")
        return v

    @field_validator('technology')
    def validate_technology(cls, v: str) -> str:
        v = v.strip()
        if len(v) > 100:
            raise ValueError("Technology name cannot exceed 100 characters.")
        return v

    @field_validator('story')
    def validate_story(cls, v: str) -> str:
        v = v.strip()
        if len(v) > 50000:
            raise ValueError("LLM responses cannot exceed 50000 characters. Please trim your response.")
        return v

    @field_validator('theme_prompt')
    def validate_theme_prompt(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        v = v.strip()
        if 0 < len(v) < 20:
            raise ValueError("Theme transformation prompts must be at least 20 characters long if provided.")
        if len(v) > 5000:
            raise ValueError("Theme transformation prompts cannot exceed 5000 characters.")
        return v

    @field_validator('theme_placeholders')
    def validate_theme_placeholders(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        v = v.strip()
        return json.dumps(json.loads(v), ensure_ascii=False, indent=2)  # Validate JSON format

    @field_validator('theme_story')
    def validate_theme_story(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        v = v.strip()
        if 0 < len(v) < 50:
            raise ValueError("Theme transformation results must be at least 50 characters long if provided.")
        if len(v) > 50000:
            raise ValueError("Theme transformation results cannot exceed 50000 characters.")
        return v

    @field_validator('education_prompt')
    def validate_education_prompt(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        v = v.strip()
        if 0 < len(v) < 20:
            raise ValueError("Educational enhancement prompts must be at least 20 characters long if provided.")
        if len(v) > 5000:
            raise ValueError("Educational enhancement prompts cannot exceed 5000 characters.")
        return v

    @field_validator('education_placeholders')
    def validate_education_placeholders(cls, v: Optional[str]) -> str:
        if not v:
            return "{}"
        v = v.strip()
        return json.dumps(json.loads(v), ensure_ascii=False, indent=2)  # Validate JSON format

    @field_validator('education_story')
    def validate_education_story(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        v = v.strip()
        if 0 < len(v) < 100:
            raise ValueError("Modified stories must be at least 100 characters long if provided. Please include the complete modified text.")
        if len(v) > 50000:
            raise ValueError("Modified stories cannot exceed 50000 characters.")
        return v

    @field_validator('questions_prompt')
    def validate_questions_prompt(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        v = v.strip()
        if 0 < len(v) < 20:
            raise ValueError("Question generation prompts must be at least 20 characters long if provided.")
        if len(v) > 5000:
            raise ValueError("Question generation prompts cannot exceed 5000 characters.")
        return v

    @field_validator('questions_placeholders')
    def validate_questions_placeholders(cls, v: Optional[str]) -> str:
        if not v:
            return "{}"
        v = v.strip()
        return json.dumps(json.loads(v), ensure_ascii=False, indent=2)  # Validate JSON format

    @field_validator('questions')
    def validate_questions(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        v = v.strip()
        if 0 < len(v) < 50:
            raise ValueError("Generated questions must be at least 50 characters long if provided. Please include complete questions.")
        if len(v) > 20000:
            raise ValueError("Generated questions cannot exceed 20000 characters.")
        return v

    @model_validator(mode='after')
    def validate_at_least_one_section(self):
        """Validate that at least one complete section is provided."""
        section1_complete = (
            len(self.prompt.strip()) >= 20 and
            len(self.technology.strip()) >= 1 and
            len(self.story.strip()) >= 100
        )

        section2_complete = (
            len((self.theme_prompt or "").strip()) >= 20 and
            len((self.theme_story or "").strip()) >= 50
        )

        section3_complete = (
            len((self.education_prompt or "").strip()) >= 20 and
            len((self.education_story or "").strip()) >= 100
        )

        section4_complete = (
            len((self.questions_prompt or "").strip()) >= 20 and
            len((self.questions or "").strip()) >= 50
        )

        if not (section1_complete or section2_complete or section3_complete or section4_complete):
            raise ValueError(
                "At least one complete section must be filled. Please complete all fields in at least one section."
            )
        return self


class LoginForm(BaseModel):
    """
    Simple login form model.
    """
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

    @field_validator('username')
    def validate_username(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Username cannot be empty.")
        if len(v) > 50:
            raise ValueError("Username cannot exceed 50 characters.")
        return v

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        if not v:
            raise ValueError("Password cannot be empty.")
        if len(v) > 200:
            raise ValueError("Password cannot exceed 200 characters.")
        return v
