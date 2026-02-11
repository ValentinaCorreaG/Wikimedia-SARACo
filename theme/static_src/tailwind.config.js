/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                /* -----------------------------
                * Brand / Neutral (Wikimedia-style)
                * ----------------------------- */
                primary: {
                    900: "#202122",
                    700: "#404244",
                    500: "#54595D",
                    300: "#A2A9B1",
                    100: "#EAECF0",
                },
        
                /* -----------------------------
                * Brand Accent (Actions & Links)
                * ----------------------------- */
                brand: {
                    700: "#3366CC",
                    500: "#447FF5",
                    300: "#99BBFF",
                    100: "#EAF2FF",
                },
        
                /* -----------------------------
                * Semantic Feedback
                * ----------------------------- */
                success: "#14866D",
                warning: "#EDAB00",
                error: "#D73333",
                info: "#2A4B8D",
        
                /* -----------------------------
                * Program / Support Colors
                * ----------------------------- */
                support: {
                    community: "#2E7D32",
                    education: "#6A1B9A",
                    culture: "#C62828",
                    technology: "#1565C0",
                    environment: "#0277BD",
                },
        
                /* -----------------------------
                * Surfaces & Backgrounds
                * ----------------------------- */
                surface: {
                    base: "#F6F5F0",
                    muted: "#F0EDE5",
                    elevated: "#FFFFFF",
                    inverse: "#202122",
                },
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('daisyui'),
    ],
    daisyui: {
        themes: [
            {
                wikimedia: {
                    /* Brand Accent – links, primary buttons */
                    "primary":          "#3366CC",
                    "primary-content":  "#FFFFFF",

                    /* Secondary – neutral UI chrome */
                    "secondary":        "#54595D",
                    "secondary-content":"#FFFFFF",

                    /* Accent – hover / highlight states */
                    "accent":           "#447FF5",
                    "accent-content":   "#FFFFFF",

                    /* Neutral – text, dark surfaces */
                    "neutral":          "#202122",
                    "neutral-content":  "#FFFFFF",

                    /* Base surfaces */
                    "base-100":         "#FFFFFF",   /* main background   */
                    "base-200":         "#F6F5F0",   /* muted / cards (cool beige)     */
                    "base-300":         "#EAE7E0",   /* borders / dividers (neutral) */
                    "base-content":     "#202122",   /* text on base      */

                    /* Semantic feedback */
                    "info":             "#2A4B8D",
                    "info-content":     "#FFFFFF",
                    "success":          "#14866D",
                    "success-content":  "#FFFFFF",
                    "warning":          "#EDAB00",
                    "warning-content":  "#202122",
                    "error":            "#D73333",
                    "error-content":    "#FFFFFF",
                    "font-family": "Inter, system-ui, sans-serif"
                },
            },
        ],
        darkTheme: false,  /* disable auto dark mode for now */
    },
}
