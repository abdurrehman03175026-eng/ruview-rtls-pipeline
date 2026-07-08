import os
import ast

class PEP8Auditor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.violations = []

    def visit_FunctionDef(self, node):
        # PEP 8 requires function names to be snake_case
        if not node.name.islower() and '_' not in node.name and node.name[0].isupper():
            self.violations.append(f"Line {node.lineno}: Function '{node.name}' should be snake_case.")
        self.generic_visit(node)

def run_style_audit():
    print("[QUALITY ASSURANCE] Commencing PEP-8 Style Verification Matrix...\n")
    target_dirs = ['week_01_telemetry', 'week_02_dsp', 'week_03_fusion', 'week_04_fingerprinting', 'week_05_automation', 'week_06_review']
    
    total_files = 0
    total_violations = 0

    for directory in target_dirs:
        if not os.path.exists(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    total_files += 1
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        try:
                            tree = ast.parse(f.read(), filename=filepath)
                            auditor = PEP8Auditor(filepath)
                            auditor.visit(tree)
                            
                            if auditor.violations:
                                print(f"⚠️ Style anomalies found in {filepath}:")
                                for v in auditor.violations:
                                    print(f"  {v}")
                                    total_violations += 1
                            else:
                                print(f"✅ {filepath} passed PEP-8 architectural naming checks.")
                        except SyntaxError:
                            print(f"❌ Syntax Error parsing {filepath}")

    print("\n" + "="*50)
    print("[AUDIT COMPLETE]")
    print(f"Total Python Source Files Audited: {total_files}")
    print(f"Total Style Violations Detected: {total_violations}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_style_audit()