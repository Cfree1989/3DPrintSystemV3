# Form Validation System Documentation

## Overview

The form validation system provides a comprehensive solution for handling form validation in both client-side and server-side contexts. It includes:

- Client-side validation with immediate feedback
- Server-side validation for data integrity
- Consistent error handling and display
- Form submission handling with AJAX support
- Form reset functionality
- Reusable validation rules and components

## Components

### 1. Form Components

The system provides several form components that can be used to build forms:

```html
{% from "shared/components/_form.html" import form, submit_button, reset_button %}
{% from "shared/components/_form_fields.html" import input_field, select_field, textarea_field, checkbox_field %}

{% call form(action=url_for('route.name'), method="POST", validation_schema={...}) %}
    {{ input_field(name='field_name', label='Field Label', ...) }}
    {{ select_field(name='field_name', label='Field Label', ...) }}
    {{ textarea_field(name='field_name', label='Field Label', ...) }}
    {{ checkbox_field(name='field_name', label='Field Label', ...) }}
    
    <div class="flex space-x-4">
        {{ submit_button(text='Submit') }}
        {{ reset_button(text='Reset') }}
    </div>
{% endcall %}
```

### 2. Validation Rules

The system includes several built-in validation rules:

- `required`: Field must not be empty
- `email`: Field must be a valid email address
- `minLength`: String must be at least N characters
- `maxLength`: String must be no more than N characters
- `number`: Value must be a valid number
- `min`: Number must be at least N
- `max`: Number must be no more than N
- `fileType`: File must be one of the allowed types
- `fileSize`: File must be less than N MB

### 3. Form Handler

The `FormHandler` class provides methods for handling form submissions:

```python
from app.utils.form_handler import FormHandler

@bp.route('/submit-form', methods=['POST'])
def submit_form():
    schema = {
        'field_name': [
            lambda v, f: validate_required(v, f),
            lambda v, f: validate_email(v, f)
        ]
    }
    
    return FormHandler.handle_form_submission(
        schema=schema,
        success_url='route.name',
        success_message='Form submitted successfully!',
        process_data=lambda data: {
            **data,
            'processed': True
        }
    )
```

## Usage Examples

### 1. Basic Form with Validation

```html
{% call form(action=url_for('route.name'), method="POST", validation_schema={
    'name': ['required', 'minLength:2', 'maxLength:50'],
    'email': ['required', 'email']
}) %}
    {{ input_field(
        name='name',
        label='Name',
        placeholder='Enter your name',
        required=true,
        validation_rules=['required', 'minLength:2', 'maxLength:50']
    ) }}
    
    {{ input_field(
        name='email',
        label='Email',
        type='email',
        placeholder='Enter your email',
        required=true,
        validation_rules=['required', 'email']
    ) }}
    
    {{ submit_button(text='Submit') }}
{% endcall %}
```

### 2. File Upload Form

```html
{% call form(action=url_for('route.upload'), method="POST", enctype="multipart/form-data") %}
    {{ input_field(
        name='file',
        label='File',
        type='file',
        required=true,
        validation_rules=['required', 'fileType:["image/jpeg", "image/png"]', 'fileSize:5']
    ) }}
    
    {{ submit_button(text='Upload') }}
{% endcall %}
```

### 3. Form with Custom Validation

```python
def validate_custom_field(value, field_name):
    if not value.startswith('custom_'):
        raise ValidationError(f"{field_name} must start with 'custom_'")

@bp.route('/submit-form', methods=['POST'])
def submit_form():
    schema = {
        'custom_field': [
            lambda v, f: validate_required(v, f),
            lambda v, f: validate_custom_field(v, f)
        ]
    }
    
    return FormHandler.handle_form_submission(
        schema=schema,
        success_url='route.name'
    )
```

## Best Practices

1. **Client-Side Validation**
   - Use immediate feedback for better user experience
   - Validate on blur and input events
   - Show clear error messages
   - Prevent form submission if validation fails

2. **Server-Side Validation**
   - Always validate on the server, even with client-side validation
   - Use consistent validation rules
   - Return clear error messages
   - Handle both AJAX and regular form submissions

3. **Error Handling**
   - Show errors inline with fields
   - Use consistent error styling
   - Provide helpful error messages
   - Handle network errors gracefully

4. **Form Reset**
   - Clear both form data and validation state
   - Reset all form fields to initial state
   - Trigger change events for proper state update

5. **Accessibility**
   - Use proper ARIA attributes
   - Ensure keyboard navigation works
   - Provide clear error announcements
   - Maintain focus management

## Integration

To integrate the validation system into existing forms:

1. Update form templates to use the new components
2. Add validation rules to form fields
3. Update route handlers to use FormHandler
4. Test both client-side and server-side validation
5. Verify error handling and form reset functionality

## Testing

The system includes a test implementation at `/validation-test` that demonstrates all features:

- Form field validation
- Error handling
- Form submission
- Form reset
- File upload
- Custom validation

Use this as a reference when implementing new forms. 