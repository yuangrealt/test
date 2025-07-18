from lxml import etree as ET
import csv
import re
import os

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
                'module': f"/({full_module})",  # 禅道格式 /() 包裹
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
                "",  # 关键词留空
                priority,
                "功能测试",
                "功能测试阶段",
                type_list if idx == 0 else "",
                stage_list if idx == 0 else ""
            ]
            writer.writerow(row)

    print(f"✅ 已生成符合禅道模板的CSV文件：{output_file}")

if __name__ == "__main__":
    input_xml = "testdemo.testproject-deep.xml"   # XML 输入
    output_csv = "zentao_template.csv"            # 输出CSV路径

    if not os.path.exists(input_xml):
        print(f"❌ XML文件未找到: {input_xml}")
    else:
        testcases = parse_testlink_xml(input_xml)
        create_zentao_template_csv(testcases, output_csv)
