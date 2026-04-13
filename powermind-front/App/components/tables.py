from nicegui import ui


def render_simple_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    ui.add_head_html('''
    <style>
        .pm-table-card {
            width: 100%;
            background: #ffffff;
            border-radius: 18px;
            padding: 12px 0 6px 0;
        }
        .pm-table-title {
            text-align: left;
            color: #3f4854;
            font-size: 1rem;
            font-weight: 700;
            padding: 0 14px 10px 14px;
        }
        .pm-table {
            width: 100%;
            border-collapse: collapse;
        }
        .pm-table thead th {
            text-align: left;
            color: #9aa3ad;
            font-size: .82rem;
            font-weight: 600;
            padding: 10px 14px;
            border-bottom: 1px solid #f0f1f3;
        }
        .pm-table tbody td {
            color: #59626d;
            font-size: .92rem;
            padding: 12px 14px;
            border-bottom: 1px solid #f6f6f7;
        }
        .pm-table tbody tr:last-child td {
            border-bottom: none;
        }
        .pm-table tbody td:last-child,
        .pm-table thead th:last-child {
            text-align: right;
        }
    </style>
    ''')

    header_html = ''.join([f'<th>{col}</th>' for col in columns])
    body_html = ''
    for row in rows:
        body_html += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'

    ui.html(
        f'<div class="pm-table-card">'
        f'<div class="pm-table-title">{title}</div>'
        f'<table class="pm-table">'
        f'<thead><tr>{header_html}</tr></thead>'
        f'<tbody>{body_html}</tbody>'
        f'</table>'
        f'</div>'
    )