console.log("FastAPI static JS loaded.");

document.addEventListener('DOMContentLoaded', function() {
    // Technology dropdown logic
    const technologySelect = document.getElementById('technology');
    const otherTechInput = document.getElementById('other-technology');

    if (technologySelect && otherTechInput) {
        updateOtherTechnologyVisibility();
        technologySelect.addEventListener('change', updateOtherTechnologyVisibility);
        function updateOtherTechnologyVisibility() {
            if (technologySelect.value === 'other') {
                otherTechInput.style.display = 'block';
                otherTechInput.required = true;
            } else {
                otherTechInput.style.display = 'none';
                otherTechInput.required = false;
            }
        }
    }

    // Original story hint
    document.querySelectorAll('textarea[name$="original_story"]').forEach(field => {
        if (!field.value) {
            field.value = "This is the original text. The prompt will be applied to it to generate the result.";
            field.classList.add("hinted");
        }
        field.addEventListener('focus', () => {
            if (field.classList.contains("hinted")) field.value = "", field.classList.remove("hinted");
        });
        field.addEventListener('blur', () => {
            if (!field.value.trim()) {
                field.value = "This is the original text. The prompt will be applied to it to generate the result.";
                field.classList.add("hinted");
            }
        });
    });

    // Section-specific prompt hints with unique samples
    const promptSamples = {
        prompt:
            "Multiple prompts? Separate with double blank lines.\n" +
            "Sample: Write a story about a sleeping child discovering a hidden forest.\n\nReveal at the end that the forest is a dream.",
        theme_prompt:
            "Multiple prompts? Separate with double blank lines.\n" +
            "Use placeholders like {gender}, {age}, {side_character}.\n" +
            "Sample: Reimagine the previous story from the viewpoint of a wise old {side_character} guiding a {age}-year-old {gender}.",
        education_prompt:
            "Multiple prompts? Separate with double blank lines.\n" +
            "Use placeholders like {gender}, {age}.\n" +
            "Sample: Add information about material properties (e.g., wood, metal) to the story and use these properties in story events and the character's decisions.",
        questions_prompt:
            "Multiple prompts? Separate with double blank lines.\n" +
            "Use placeholders like {gender}, {age}.\n" +
            "Sample: Generate three questions that check the listener's knowledge about the material properties mentioned in the story."
    };

    Object.entries(promptSamples).forEach(([name, sample]) => {
        document.querySelectorAll(`textarea[name="${name}"]`).forEach(field => {
            if (!field.value) {
                field.value = sample;
                field.classList.add("hinted");
            }
            field.addEventListener('focus', () => {
                if (field.classList.contains("hinted")) field.value = "", field.classList.remove("hinted");
            });
            field.addEventListener('blur', () => {
                if (!field.value.trim()) {
                    field.value = sample;
                    field.classList.add("hinted");
                }
            });
        });
    });

    // Placeholders fields hint matching prompts
    const placeholderSamples = {
        theme_placeholders: '{"gender": "boy", "age": "8", "side_character": "owl"}',
        education_placeholders: '{"gender": "girl", "age": "10"}'
    };

    Object.entries(placeholderSamples).forEach(([name, sample]) => {
        document.querySelectorAll(`textarea[name="${name}"]`).forEach(field => {
            if (!field.value) {
                field.value = "Use the JSON placeholders you used to generate the current story.\nExample: " + sample;
                field.classList.add("hinted");
            }
            field.addEventListener('focus', () => {
                if (field.classList.contains("hinted")) field.value = "", field.classList.remove("hinted");
            });
            field.addEventListener('blur', () => {
                if (!field.value.trim()) {
                    field.value = "Use the JSON placeholders you used to generate the current story.\nExample: " + sample;
                    field.classList.add("hinted");
                }
            });
        });
    });

    // Story (generated) fields hint
    ["story", "theme_story", "education_story", "questions"].forEach(name => {
        document.querySelectorAll(`textarea[name="${name}"]`).forEach(field => {
            if (!field.value) {
                field.value = "This should be the final output of the LLM.";
                field.classList.add("hinted");
            }
            field.addEventListener('focus', () => {
                if (field.classList.contains("hinted")) field.value = "", field.classList.remove("hinted");
            });
            field.addEventListener('blur', () => {
                if (!field.value.trim()) {
                    field.value = "This should be the final output of the LLM.";
                    field.classList.add("hinted");
                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // ...your other JS...

    // Before form submit: clear all .hinted fields
    document.querySelectorAll('form.submission-form').forEach(function(form) {
        form.addEventListener('submit', function() {
            form.querySelectorAll('textarea.hinted').forEach(function(field) {
                // Only clear if hint is shown (i.e., user didn't edit it)
                field.value = '';
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('form.submission-form');
    if (!form) return;

    // Remove any old category/category fields (for safety on re-edit)
    Array.from(form.querySelectorAll('input[name="category"],input[name="categories"]')).forEach(el => el.remove());

    form.addEventListener('submit', function(e) {
        // Helper: section fully filled?
        function filled(names) {
            return names.every(name => {
                var el = form.querySelector(`[name="${name}"]`);
                return el && el.value && el.value.trim().length > 0;
            });
        }

        // Collect filled categories
        let filledSections = [];
        if (filled(['prompt', 'story', 'technology'])) filledSections.push('story');
        if (filled(['theme_prompt', 'theme_placeholders', 'theme_story', 'technology', 'theme_original_story'])) filledSections.push('theme');
        if (filled(['education_prompt', 'education_placeholders', 'education_story', 'technology', 'education_original_story'])) filledSections.push('education');
        if (filled(['questions_prompt', 'questions', 'technology', 'questions_original_story'])) filledSections.push('questions');

        // Remove old categories fields
        Array.from(form.querySelectorAll('input[name="categories"]')).forEach(el => el.remove());

        if (filledSections.length === 0) {
            e.preventDefault();
            alert("Please fully fill at least one section before submitting.");
            return;
        }

        // Add one hidden field per filled section
        filledSections.forEach(cat => {
            let inp = document.createElement('input');
            inp.type = 'hidden';
            inp.name = 'categories';
            inp.value = cat;
            form.appendChild(inp);
        });
    });
});

