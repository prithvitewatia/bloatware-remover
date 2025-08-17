# Bloatware Remover Templates

This directory contains the HTML templates for the Bloatware Remover web application, built with Bootstrap 5 and optimized with reusable components.

## Structure

```
templates/
├── base.html              # Base template with Bootstrap 5, navigation, and common layout
├── connect.html           # Device connection form
├── packages.html          # Package management interface
├── status.html            # Operation status display
├── components/            # Reusable template components
│   ├── alert.html         # Alert component
│   ├── form_field.html    # Form field component
│   └── card.html          # Card component
└── README.md              # This file
```

## Base Template (`base.html`)

The base template provides:
- Bootstrap 5 CSS and JS integration
- Bootstrap Icons
- Responsive navigation bar
- Consistent footer
- Custom CSS styling
- Responsive viewport meta tag

### Features:
- **Navigation**: Clean navigation with icons and responsive mobile menu
- **Footer**: Professional footer with branding
- **Styling**: Custom CSS for enhanced visual appeal
- **Responsive**: Mobile-first responsive design

## Components

### Alert Component (`components/alert.html`)
Reusable alert component with different types and icons.

**Usage:**
```jinja2
{% from "components/alert.html" import alert %}
{{ alert("success", "Title", "Message", true) }}
```

**Parameters:**
- `type`: Alert type (success, danger, warning, info)
- `title`: Alert title (optional)
- `message`: Alert message
- `dismissible`: Whether alert can be dismissed (default: true)

### Form Field Component (`components/form_field.html`)
Reusable form field with consistent styling.

**Usage:**
```jinja2
{% from "components/form_field.html" import form_field %}
{{ form_field("text", "field_name", "field_id", "Label", "placeholder", true, "help text", "icon") }}
```

**Parameters:**
- `field_type`: Input type (text, email, password, etc.)
- `field_name`: Form field name
- `field_id`: Form field ID
- `label`: Field label
- `placeholder`: Placeholder text (optional)
- `required`: Whether field is required (default: false)
- `help_text`: Help text below field (optional)
- `icon`: Bootstrap icon name (optional)

### Card Component (`components/card.html`)
Reusable card component with header and body.

**Usage:**
```jinja2
{% from "components/card.html" import card %}
{% call card("Title", "icon-name") %}
    Card content here
{% endcall %}
```

**Parameters:**
- `title`: Card title
- `icon`: Bootstrap icon name (optional)
- `header_class`: CSS classes for header (default: "bg-primary text-white")

## Templates

### Connect Template (`connect.html`)
Device connection interface with:
- Connection instructions
- Form fields for IP, port, and pairing code
- Error handling
- Responsive design

### Packages Template (`packages.html`)
Package management interface with:
- Table view of installed packages
- Action selection (disable/uninstall)
- Bulk action buttons
- Package count display
- JavaScript for bulk operations

### Status Template (`status.html`)
Operation status display with:
- Success/error status indicators
- Large icons for visual feedback
- Navigation buttons
- Centered layout

## Bootstrap 5 Features Used

- **Grid System**: Responsive columns and rows
- **Components**: Cards, alerts, buttons, forms, tables, navigation
- **Utilities**: Spacing, colors, typography, flexbox
- **Icons**: Bootstrap Icons integration
- **JavaScript**: Collapsible navigation, dismissible alerts

## Custom Styling

The templates include custom CSS for:
- Enhanced card shadows
- Improved button hover states
- Better form focus states
- Consistent alert styling
- Clean list group appearance

## Responsive Design

All templates are mobile-first and responsive:
- Navigation collapses on mobile
- Tables become scrollable on small screens
- Buttons stack appropriately
- Forms adapt to screen size

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers
- Bootstrap 5 compatibility
- Progressive enhancement approach 