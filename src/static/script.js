console.log("FastAPI static JS loaded.");

document.addEventListener('DOMContentLoaded', function() {
    // Technology dropdown logic
    const techSel = document.getElementById('technology');
    const otherTech = document.getElementById('other-technology');
    if (techSel && otherTech) {
        function updateTech() {
            if (techSel.value === 'other') {
                otherTech.style.display = 'block';
                otherTech.required = true;
            } else {
                otherTech.style.display = 'none';
                otherTech.required = false;
            }
        }
        updateTech();
        techSel.addEventListener('change', updateTech);
    }

    // Generic hint helper
    function setHint(field, hint) {
        if (!field.value) {
            field.value = hint;
            field.classList.add("hinted");
        }
        field.addEventListener('focus', () => {
            if (field.classList.contains("hinted")) {
                field.value = "";
                field.classList.remove("hinted");
            }
        });
        field.addEventListener('blur', () => {
            if (!field.value.trim()) {
                field.value = hint;
                field.classList.add("hinted");
            }
        });
    }

    // Prompt hints per section
    const promptSamples = {
        prompt:
            "Multiple prompts? Separate with double blank lines.\n" +
            "Sample: Write a story about a sleeping child discovering a hidden forest.\n\nReveal at the end that the forest is a dream.",
        theme_prompt:
            "Multiple prompts? Separate with double blank lines.\n" +
            "Use placeholders like {gender}, {age}, {side_character}.\n" +
            "Sample: Reimagine the previous story from the viewpoint of a wise old {side_character} guiding a {age}-year-old {gender}.",
        education_prompt:
            "Multiple prompts? Separate with double blank lines. Use placeholders {age}.\n" +
            "Sample: Add information about material properties (e.g., wood, metal) to the story and use these properties in story events and the character's decisions. Information should be relevant to {age}-old child.",
        questions_prompt:
            "Multiple prompts? Separate with double blank lines.\n" +
            "Use placeholders like {gender}, {age}.\n" +
            "Sample: Generate three questions and responses as a JSON dict that check the listener's knowledge about the material properties mentioned in the story.\n\n" +
            "LLM response example:\n" +
            "{\"Why did he select an iron sword instead a gold one?\": \"Iron is harder than gold, golden one would break\"}"
    };

    Object.entries(promptSamples).forEach(([name, sample]) => {
        document.querySelectorAll(`textarea[name="${name}"]`).forEach(field => setHint(field, sample));
    });

    // Placeholder JSON hints
    const placeholderSamples = {
        theme_placeholders:
            'Use the JSON placeholders you used to generate the current story.\nExample: {"gender": "boy", "age": "8", "side_character": "owl"}',
        education_placeholders:
            'Use the JSON placeholders you used to generate the current story.\nExample: {"gender": "girl", "age": "10"}'
    };

    Object.entries(placeholderSamples).forEach(([name, sample]) => {
        document.querySelectorAll(`textarea[name="${name}"]`).forEach(field => setHint(field, sample));
    });

    // Original story fields
    document.querySelectorAll('textarea[name$="original_story"]').forEach(field =>
        setHint(field, "This is the original text. The prompt will be applied to it to generate the result.")
    );

    // Story-like output fields
    ["story", "theme_story", "education_story"].forEach(name => {
        document.querySelectorAll(`textarea[name="${name}"]`).forEach(field =>
            setHint(field, "This should be the final output of the LLM.")
        );
    });

    // Questions field: special JSON example
    document.querySelectorAll(`textarea[name="questions"]`).forEach(field => {
        const qSample = "Provide questions + answers as JSON.\nExample: " +
            '{"Why did he select an iron sword instead a gold one?": "Iron is harder than gold, golden one would break"}';
        setHint(field, qSample);
    });

    // Submission form logic
    document.querySelectorAll('form.submission-form').forEach(form => {
        // Clean up old hidden inputs on load
        Array.from(form.querySelectorAll('input[name="category"],input[name="categories"]')).forEach(el => el.remove());

        form.addEventListener('submit', function(e) {
            // Clear hinted values before submit
            form.querySelectorAll('textarea.hinted').forEach(field => field.value = '');

            // Section fully filled?
            function filled(names) {
                return names.every(name => {
                    const el = form.querySelector(`[name="${name}"]`);
                    return el && el.value && el.value.trim().length > 0;
                });
            }

            const filledSections = [];
            if (filled(['prompt', 'story', 'technology'])) filledSections.push('story');
            if (filled(['theme_prompt', 'theme_placeholders', 'theme_story', 'technology', 'theme_original_story'])) filledSections.push('theme');
            if (filled(['education_prompt', 'education_placeholders', 'education_story', 'technology', 'education_original_story'])) filledSections.push('education');
            if (filled(['questions_prompt', 'questions', 'technology', 'questions_original_story'])) filledSections.push('questions');

            if (!filledSections.length) {
                e.preventDefault();
                alert("Please fully fill at least one section before submitting.");
                return;
            }

            // Inject hidden input(s)
            filledSections.forEach(cat => {
                const inp = document.createElement('input');
                inp.type = 'hidden';
                inp.name = 'categories';
                inp.value = cat;
                form.appendChild(inp);
            });
        });
    });
});
