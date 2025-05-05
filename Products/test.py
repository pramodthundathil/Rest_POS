from graphviz import Digraph

# Create a use case diagram
use_case_diagram = Digraph('UseCaseDiagram', format='png')
use_case_diagram.attr(dpi='300')

# Define actors
use_case_diagram.node('Student', shape='actor', label='👨‍🎓 Student')
use_case_diagram.node('Educator', shape='actor', label='👨‍🏫 Educator')
use_case_diagram.node('Admin', shape='actor', label='🛠️ Admin')
use_case_diagram.node('MLModel', shape='ellipse', label='🤖 Machine Learning Model')

# Define use cases
use_cases = {
    "UC1": "User Registration & Authentication",
    "UC2": "Upload Academic Data",
    "UC3": "Predict CGPA",
    "UC4": "View Predicted Results & Trends",
    "UC5": "Generate Reports",
    "UC6": "Send Notifications & Alerts",
    "UC7": "Manage Users"
}

for uc_id, uc_label in use_cases.items():
    use_case_diagram.node(uc_id, shape='ellipse', label=uc_label)

# Connect actors to use cases
use_case_diagram.edge('Student', 'UC1')
use_case_diagram.edge('Student', 'UC2')
use_case_diagram.edge('Student', 'UC3')
use_case_diagram.edge('Student', 'UC4')
use_case_diagram.edge('Educator', 'UC1')
use_case_diagram.edge('Educator', 'UC4')
use_case_diagram.edge('Educator', 'UC5')
use_case_diagram.edge('Educator', 'UC6')
use_case_diagram.edge('Admin', 'UC1')
use_case_diagram.edge('Admin', 'UC7')
use_case_diagram.edge('MLModel', 'UC3')

# Render diagram
diagram_path = "/student_result_prediction_use_case.png"
use_case_diagram.render(diagram_path, format='png', cleanup=True)
diagram_path
