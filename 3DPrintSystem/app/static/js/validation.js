// Validation utility functions
const validationRules = {
    required: (value) => ({
        isValid: value !== undefined && value !== null && value !== '',
        message: 'This field is required'
    }),
    
    email: (value) => ({
        isValid: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
        message: 'Please enter a valid email address'
    }),
    
    minLength: (min) => (value) => ({
        isValid: value.length >= min,
        message: `Must be at least ${min} characters`
    }),
    
    maxLength: (max) => (value) => ({
        isValid: value.length <= max,
        message: `Must be no more than ${max} characters`
    }),
    
    fileType: (allowedTypes) => (file) => ({
        isValid: allowedTypes.includes(file.type),
        message: `File must be one of: ${allowedTypes.join(', ')}`
    }),
    
    fileSize: (maxSizeMB) => (file) => ({
        isValid: file.size <= maxSizeMB * 1024 * 1024,
        message: `File size must be less than ${maxSizeMB}MB`
    }),
    
    number: (value) => ({
        isValid: !isNaN(value) && value !== '',
        message: 'Please enter a valid number'
    }),
    
    min: (min) => (value) => ({
        isValid: Number(value) >= min,
        message: `Must be at least ${min}`
    }),
    
    max: (max) => (value) => ({
        isValid: Number(value) <= max,
        message: `Must be no more than ${max}`
    })
};

// Validation state management
class ValidationManager {
    constructor() {
        this.errors = {};
        this.touched = {};
    }

    validateField(fieldName, value, rules) {
        this.touched[fieldName] = true;
        this.errors[fieldName] = null;

        for (const rule of rules) {
            const result = rule(value);
            if (!result.isValid) {
                this.errors[fieldName] = result.message;
                break;
            }
        }

        return !this.errors[fieldName];
    }

    validateForm(formData, validationSchema) {
        let isValid = true;
        this.errors = {};

        for (const [fieldName, rules] of Object.entries(validationSchema)) {
            const value = formData[fieldName];
            if (!this.validateField(fieldName, value, rules)) {
                isValid = false;
            }
        }

        return isValid;
    }

    getFieldError(fieldName) {
        return this.errors[fieldName];
    }

    isFieldTouched(fieldName) {
        return this.touched[fieldName];
    }

    reset() {
        this.errors = {};
        this.touched = {};
    }
}

// Export validation utilities
window.validationRules = validationRules;
window.ValidationManager = ValidationManager; 