import os
import csv
import re
from lxml import etree as ET

def remove_html_tags(text):
    if text is None:
        return ""
    text = text.replace('<p>', '\n').replace('</p>', '\n')
    text = text.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    text = text.replace('&nbsp;', ' ')
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def parse_testlink_xml(xml_file):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(xml_file, parser)
    root = tree.getroot()
    testcases = []

    def extract_testcases(suite, module_stack):
        module_name = suite.get('name') or "未命名模块"
        module_stack.append(module_name)
        full_module = "/".join(module_stack)

        for testcase in suite.findall('testcase'):
            case_data = {
                'module': f"/({full_module})",
                'title': testcase.get('name'),
                'steps': [],
                'preconditions': remove_html_tags(testcase.findtext('preconditions')),
                'summary': remove_html_tags(testcase.findtext('summary')),
                'importance': testcase.findtext('importance', '2')
            }

            steps = testcase.find('steps')
            if steps is not None:
                for step in steps.findall('step'):
                    actions = remove_html_tags(step.findtext('actions'))
                    expected = remove_html_tags(step.findtext('expectedresults'))
                    case_data['steps'].append({
                        'actions': actions,
                        'expected': expected
                    })

            testcases.append(case_data)

        for child_suite in suite.findall('testsuite'):
            extract_testcases(child_suite, module_stack.copy())

    extract_testcases(root, [])
    return testcases

def create_zentao_template_csv(testcases, output_file):
    headers = [
        "所属模块", "用例名称", "前置条件", "步骤", "预期", "关键词",
        "优先级", "用例类型", "适用阶段", "类型可选值列表", "阶段可选值列表"
    ]
    type_list = "单元测试\n接口测试\n功能测试\n安装部署\n配置相关\n性能测试\n安全相关\n其他"
    stage_list = "单元测试阶段\n功能测试阶段\n集成测试阶段\n系统测试阶段\n冒烟测试阶段\n版本验证阶段"

    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for idx, case in enumerate(testcases):
            steps_str = "\n".join(f"{i+1}. {s['actions']}" for i, s in enumerate(case['steps']))
            expected_str = "\n".join(f"{i+1}. {s['expected']}" for i, s in enumerate(case['steps']))
            priority_map = {'1': '3', '2': '2', '3': '1'}
            priority = priority_map.get(case['importance'], '2')

            row = [
                case['module'],
                case['title'],
                case['preconditions'] or case['summary'],
                steps_str.strip(),
                expected_str.strip(),
                "",
                priority,
                "功能测试",
                "功能测试阶段",
                type_list if idx == 0 else "",
                stage_list if idx == 0 else ""
            ]
            writer.writerow(row)

def batch_convert_xml_to_csv():
    current_dir = os.getcwd()
    xml_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.xml')]

    if not xml_files:
        print("⚠️ 当前目录下未找到 .xml 文件。")
        return

    for xml_file in xml_files:
        try:
            print(f"🚀 正在转换：{xml_file}")
            testcases = parse_testlink_xml(xml_file)
            csv_file = os.path.splitext(xml_file)[0] + ".csv"
            create_zentao_template_csv(testcases, csv_file)
            print(f"✅ 已生成：{csv_file}")
        except Exception as e:
            print(f"❌ 转换失败：{xml_file}，错误信息：{e}")

if __name__ == "__main__":
    batch_convert_xml_to_csv()
