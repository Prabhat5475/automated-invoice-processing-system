
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side
)
from openpyxl.chart import (
    BarChart, DoughnutChart, Reference
)
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.utils import get_column_letter

from db_connection import create_connection


# -----------------------------------------
# DASHBOARD COLOURS
# -----------------------------------------

NAVY = "23364D"
TEAL = "00A99D"
BLUE = "3686B7"
GREEN = "239B75"
ORANGE = "E8A838"
WHITE = "FFFFFF"
BLACK = "000000"
LIGHT_BG = "F3F6FA"
GREY = "64748B"

CURRENCY_FORMAT = '"₹"#,##0.00'


def export_reports():

    connection = create_connection()

    if connection is None:
        print("Cannot export dashboard: Database connection failed.")
        return

    cursor = None

    try:

        cursor = connection.cursor()

        # -----------------------------------------
        # 1. FETCH DATA FROM MYSQL
        # -----------------------------------------

        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(amount), 0)
            FROM invoices
        """)

        total_invoices, total_revenue = cursor.fetchone()
        total_revenue = float(total_revenue)

        cursor.execute("""
            SELECT status, COUNT(*), COALESCE(SUM(amount), 0)
            FROM invoices
            GROUP BY status
        """)

        payment_data = cursor.fetchall()

        payment = {
            status: {
                "count": count,
                "amount": float(amount)
            }
            for status, count, amount in payment_data
        }

        paid_amount = payment.get("PAID", {}).get("amount", 0)
        pending_amount = payment.get("PENDING", {}).get("amount", 0)

        paid_count = payment.get("PAID", {}).get("count", 0)
        pending_count = payment.get("PENDING", {}).get("count", 0)

        cursor.execute("""
            SELECT customer_name, COUNT(*), SUM(amount)
            FROM invoices
            GROUP BY customer_name
            ORDER BY SUM(amount) DESC
        """)

        customers = cursor.fetchall()

        cursor.execute("""
            SELECT DATE_FORMAT(invoice_date, '%Y-%m'),
                   SUM(amount)
            FROM invoices
            GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
            ORDER BY DATE_FORMAT(invoice_date, '%Y-%m')
        """)

        monthly_data = cursor.fetchall()

        # -----------------------------------------
        # 2. CREATE WORKBOOK
        # -----------------------------------------

        workbook = Workbook()

        dashboard = workbook.active
        dashboard.title = "Invoice Dashboard"

        data_sheet = workbook.create_sheet("Chart Data")

        dashboard.sheet_view.showGridLines = False
        dashboard.sheet_view.zoomScale = 75

        # -----------------------------------------
        # 3. DASHBOARD BACKGROUND AND DIMENSIONS
        # -----------------------------------------

        for col in range(1, 17):
            dashboard.column_dimensions[
                get_column_letter(col)
            ].width = 12

        # Wider columns for readable tables
        dashboard.column_dimensions["A"].width = 22
        dashboard.column_dimensions["B"].width = 15
        dashboard.column_dimensions["C"].width = 19

        dashboard.column_dimensions["H"].width = 25
        dashboard.column_dimensions["I"].width = 15
        dashboard.column_dimensions["J"].width = 19

        for row in range(1, 56):
            dashboard.row_dimensions[row].height = 21

            for col in range(1, 17):
                dashboard.cell(row, col).fill = PatternFill(
                    "solid",
                    fgColor=LIGHT_BG
                )

        # -----------------------------------------
        # 4. DASHBOARD TITLE
        # -----------------------------------------

        dashboard.merge_cells("A1:P1")
        dashboard["A1"] = "INVOICE ANALYTICS DASHBOARD"

        dashboard["A1"].font = Font(
            name="Arial",
            size=22,
            bold=True,
            color=WHITE
        )

        dashboard["A1"].fill = PatternFill(
            "solid",
            fgColor=NAVY
        )

        dashboard["A1"].alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        dashboard.row_dimensions[1].height = 43

        dashboard.merge_cells("A2:P2")
        dashboard["A2"] = (
            "FINANCIAL PERFORMANCE | PRABHAT TECHNOLOGIES"
        )

        dashboard["A2"].font = Font(
            name="Arial",
            size=10,
            italic=True,
            color=GREY
        )

        dashboard["A2"].alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        # -----------------------------------------
        # 5. KPI CARDS
        # -----------------------------------------

        def create_card(
            label_range,
            value_range,
            label,
            value,
            color,
            number_format=None
        ):

            dashboard.merge_cells(label_range)
            dashboard.merge_cells(value_range)

            label_cell = dashboard[label_range.split(":")[0]]
            value_cell = dashboard[value_range.split(":")[0]]

            label_cell.value = label
            value_cell.value = value

            for cell_range in [label_range, value_range]:
                for row in dashboard[cell_range]:
                    for cell in row:
                        cell.fill = PatternFill(
                            "solid",
                            fgColor=color
                        )

            label_cell.font = Font(
                name="Arial",
                size=10,
                bold=True,
                color=WHITE
            )

            value_cell.font = Font(
                name="Arial",
                size=19,
                bold=True,
                color=WHITE
            )

            label_cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

            value_cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

            if number_format:
                value_cell.number_format = number_format

        create_card(
            "A4:D4", "A5:D6",
            "TOTAL REVENUE",
            total_revenue,
            NAVY,
            CURRENCY_FORMAT
        )

        create_card(
            "E4:H4", "E5:H6",
            "TOTAL INVOICES",
            total_invoices,
            BLUE
        )

        create_card(
            "I4:L4", "I5:L6",
            "PAID AMOUNT",
            paid_amount,
            GREEN,
            CURRENCY_FORMAT
        )

        create_card(
            "M4:P4", "M5:P6",
            "PENDING AMOUNT",
            pending_amount,
            ORANGE,
            CURRENCY_FORMAT
        )

        dashboard.row_dimensions[4].height = 26
        dashboard.row_dimensions[5].height = 28
        dashboard.row_dimensions[6].height = 28

        # -----------------------------------------
        # 6. PREPARE CHART DATA
        # -----------------------------------------

        data_sheet.append(["Status", "Amount"])
        data_sheet.append(["PAID", paid_amount])
        data_sheet.append(["PENDING", pending_amount])

        data_sheet["D1"] = "Customer"
        data_sheet["E1"] = "Revenue"
        data_sheet["F1"] = "Invoice Count"

        for row_number, (customer, count, amount) in enumerate(
            customers, start=2
        ):

            data_sheet.cell(row_number, 4, customer)
            data_sheet.cell(row_number, 5, float(amount))
            data_sheet.cell(row_number, 6, count)

        data_sheet["H1"] = "Month"
        data_sheet["I1"] = "Revenue"

        for row_number, (month, amount) in enumerate(
            monthly_data, start=2
        ):

            data_sheet.cell(row_number, 8, month)
            data_sheet.cell(row_number, 9, float(amount))

        # -----------------------------------------
        # 7. CHART SECTION HEADINGS
        # -----------------------------------------

        sections = [
            ("A8:H8", "MONTHLY REVENUE"),
            ("I8:P8", "PAYMENT DISTRIBUTION"),
            ("A24:H24", "CUSTOMER-WISE REVENUE"),
            ("I24:P24", "INVOICE COUNT BY CUSTOMER")
        ]

        for cell_range, heading in sections:

            dashboard.merge_cells(cell_range)

            cell = dashboard[cell_range.split(":")[0]]
            cell.value = heading

            cell.font = Font(
                bold=True,
                size=12,
                color=WHITE
            )

            cell.fill = PatternFill(
                "solid",
                fgColor=TEAL
            )

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

        # -----------------------------------------
        # 8. MONTHLY REVENUE CHART
        # -----------------------------------------

        if monthly_data:

            monthly_chart = BarChart()

            monthly_chart.type = "col"
            monthly_chart.style = 10
            monthly_chart.title = "Monthly Revenue"

            # Keep numerical markings visible.
            # Remove axis titles that were overlapping the chart.
            monthly_chart.x_axis.tickLblPos = "low"
            monthly_chart.y_axis.tickLblPos = "nextTo"

            monthly_chart.y_axis.numFmt = '"₹"#,##0'
            monthly_chart.y_axis.scaling.min = 0

            monthly_chart.height = 7.2
            monthly_chart.width = 14.2

            monthly_values = Reference(
                data_sheet,
                min_col=9,
                min_row=1,
                max_row=len(monthly_data) + 1
            )

            monthly_categories = Reference(
                data_sheet,
                min_col=8,
                min_row=2,
                max_row=len(monthly_data) + 1
            )

            monthly_chart.add_data(
                monthly_values,
                titles_from_data=True
            )

            monthly_chart.set_categories(monthly_categories)

            monthly_chart.legend = None

            monthly_chart.series[
                0
            ].graphicalProperties.solidFill = BLUE

            dashboard.add_chart(monthly_chart, "A9")

        # -----------------------------------------
        # 9. PAYMENT DOUGHNUT CHART
        # -----------------------------------------

        payment_chart = DoughnutChart()

        payment_chart.title = "Paid vs Pending"
        payment_chart.style = 10
        payment_chart.height = 7.2
        payment_chart.width = 14.2
        payment_chart.holeSize = 60

        payment_values = Reference(
            data_sheet,
            min_col=2,
            min_row=1,
            max_row=3
        )

        payment_categories = Reference(
            data_sheet,
            min_col=1,
            min_row=2,
            max_row=3
        )

        payment_chart.add_data(
            payment_values,
            titles_from_data=True
        )

        payment_chart.set_categories(payment_categories)

        # Display percentages only
        payment_chart.dataLabels = DataLabelList()
        payment_chart.dataLabels.showPercent = True
        payment_chart.dataLabels.showVal = False
        payment_chart.dataLabels.showCatName = False
        payment_chart.dataLabels.showLeaderLines = True

        # Black outlines around each doughnut segment
        black_outline = LineProperties(
            solidFill=BLACK,
            w=19050
        )

        payment_chart.series[0].data_points = [
            DataPoint(
                idx=0,
                spPr=GraphicalProperties(
                    solidFill=GREEN,
                    ln=black_outline
                )
            ),
            DataPoint(
                idx=1,
                spPr=GraphicalProperties(
                    solidFill=ORANGE,
                    ln=black_outline
                )
            )
        ]

        # Border around the chart area
        payment_chart.graphicalProperties = GraphicalProperties(
            solidFill=WHITE,
            ln=LineProperties(
                solidFill=BLACK,
                w=19050
            )
        )

        dashboard.add_chart(payment_chart, "I9")

        # -----------------------------------------
        # 10. CUSTOMER REVENUE BAR CHART
        # -----------------------------------------

        if customers:

            last_row = len(customers) + 1

            revenue_chart = BarChart()

            revenue_chart.type = "bar"
            revenue_chart.style = 10
            revenue_chart.title = "Revenue by Customer"

            # Numerical scale at the bottom
            # Customer names outside the bars
            revenue_chart.x_axis.tickLblPos = "low"
            revenue_chart.y_axis.tickLblPos = "nextTo"

            revenue_chart.x_axis.numFmt = '"₹"#,##0'
            revenue_chart.x_axis.scaling.min = 0

            # Remove axis titles to prevent text overlapping bars
            revenue_chart.height = 7.2
            revenue_chart.width = 14.2

            revenue_values = Reference(
                data_sheet,
                min_col=5,
                min_row=1,
                max_row=last_row
            )

            revenue_categories = Reference(
                data_sheet,
                min_col=4,
                min_row=2,
                max_row=last_row
            )

            revenue_chart.add_data(
                revenue_values,
                titles_from_data=True
            )

            revenue_chart.set_categories(revenue_categories)
            revenue_chart.legend = None

            revenue_chart.series[
                0
            ].graphicalProperties.solidFill = TEAL

            dashboard.add_chart(revenue_chart, "A25")

            # -------------------------------------
            # 11. INVOICE COUNT BAR CHART
            # -------------------------------------

            count_chart = BarChart()

            count_chart.type = "bar"
            count_chart.style = 10
            count_chart.title = "Invoices by Customer"

            count_chart.x_axis.tickLblPos = "low"
            count_chart.y_axis.tickLblPos = "nextTo"

            count_chart.x_axis.numFmt = "0"
            count_chart.x_axis.scaling.min = 0

            count_chart.height = 7.2
            count_chart.width = 14.2

            count_values = Reference(
                data_sheet,
                min_col=6,
                min_row=1,
                max_row=last_row
            )

            count_categories = Reference(
                data_sheet,
                min_col=4,
                min_row=2,
                max_row=last_row
            )

            count_chart.add_data(
                count_values,
                titles_from_data=True
            )

            count_chart.set_categories(count_categories)
            count_chart.legend = None

            count_chart.series[
                0
            ].graphicalProperties.solidFill = BLUE

            dashboard.add_chart(count_chart, "I25")

        # -----------------------------------------
        # 12. TABLE FORMATTING HELPER
        # -----------------------------------------

        thin_side = Side(
            style="thin",
            color="AAB7C4"
        )

        medium_side = Side(
            style="medium",
            color=NAVY
        )

        table_border = Border(
            left=thin_side,
            right=thin_side,
            top=thin_side,
            bottom=thin_side
        )

        outer_border = Border(
            left=medium_side,
            right=medium_side,
            top=medium_side,
            bottom=medium_side
        )

        def format_table(
            title_range,
            title,
            header_row,
            start_col,
            end_col,
            last_row
        ):

            dashboard.merge_cells(title_range)

            title_cell = dashboard[
                title_range.split(":")[0]
            ]

            title_cell.value = title
            title_cell.font = Font(
                bold=True,
                size=11,
                color=WHITE
            )

            title_cell.fill = PatternFill(
                "solid",
                fgColor=TEAL
            )

            title_cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

            # Style header row
            for col in range(start_col, end_col + 1):

                cell = dashboard.cell(header_row, col)

                cell.font = Font(
                    bold=True,
                    color=WHITE,
                    size=10
                )

                cell.fill = PatternFill(
                    "solid",
                    fgColor=NAVY
                )

                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                    wrap_text=True
                )

            # Add borders and clean formatting
            for row in range(header_row, last_row + 1):

                for col in range(start_col, end_col + 1):

                    cell = dashboard.cell(row, col)

                    cell.border = table_border
                    cell.alignment = Alignment(
                        vertical="center",
                        horizontal="center"
                    )

            # Add a stronger outer boundary
            for col in range(start_col, end_col + 1):

                dashboard.cell(
                    header_row, col
                ).border = Border(
                    top=medium_side,
                    bottom=thin_side,
                    left=medium_side if col == start_col else thin_side,
                    right=medium_side if col == end_col else thin_side
                )

                dashboard.cell(
                    last_row, col
                ).border = Border(
                    bottom=medium_side,
                    left=medium_side if col == start_col else thin_side,
                    right=medium_side if col == end_col else thin_side
                )

            for row in range(header_row + 1, last_row):

                dashboard.cell(
                    row, start_col
                ).border = Border(
                    left=medium_side,
                    right=thin_side,
                    top=thin_side,
                    bottom=thin_side
                )

                dashboard.cell(
                    row, end_col
                ).border = Border(
                    right=medium_side,
                    left=thin_side,
                    top=thin_side,
                    bottom=thin_side
                )

        # -----------------------------------------
        # 13. PAYMENT SUMMARY TABLE
        # -----------------------------------------

        payment_headers = [
            "Status",
            "Invoice Count",
            "Total Amount"
        ]

        for col, header in enumerate(payment_headers, start=1):
            dashboard.cell(43, col, header)

        payment_rows = [
            ("PAID", paid_count, paid_amount),
            ("PENDING", pending_count, pending_amount)
        ]

        for row_number, row_data in enumerate(
            payment_rows, start=44
        ):

            for col, value in enumerate(row_data, start=1):
                dashboard.cell(row_number, col, value)

            dashboard.cell(
                row_number, 3
            ).number_format = CURRENCY_FORMAT

        format_table(
            "A42:C42",
            "PAYMENT SUMMARY",
            43,
            1,
            3,
            45
        )

        # -----------------------------------------
        # 14. CUSTOMER SUMMARY TABLE
        # -----------------------------------------

        customer_headers = [
            "Customer",
            "Invoice Count",
            "Total Revenue"
        ]

        for col, header in enumerate(
            customer_headers, start=8
        ):
            dashboard.cell(43, col, header)

        for row_number, (customer, count, amount) in enumerate(
            customers, start=44
        ):

            dashboard.cell(row_number, 8, customer)
            dashboard.cell(row_number, 9, count)
            dashboard.cell(row_number, 10, float(amount))

            dashboard.cell(
                row_number, 10
            ).number_format = CURRENCY_FORMAT

        customer_last_row = 43 + len(customers)

        format_table(
            "H42:J42",
            "CUSTOMER SUMMARY",
            43,
            8,
            10,
            customer_last_row
        )

        # -----------------------------------------
        # 15. FINAL WORKSHEET SETTINGS
        # -----------------------------------------

        data_sheet.sheet_state = "hidden"

        dashboard.freeze_panes = "A4"

        dashboard.sheet_properties.pageSetUpPr.fitToPage = True
        dashboard.page_setup.orientation = "landscape"
        dashboard.page_setup.fitToWidth = 1
        dashboard.page_setup.fitToHeight = 1

        dashboard.print_area = "A1:P55"

        # -----------------------------------------
        # 16. SAVE DASHBOARD
        # -----------------------------------------

        project_folder = Path(__file__).resolve().parent.parent

        output_folder = project_folder / "data" / "output"
        output_folder.mkdir(parents=True, exist_ok=True)

        output_file = output_folder / "Invoice_Reports.xlsx"

        workbook.save(output_file)

        print("\nProfessional Invoice Dashboard generated successfully!")
        print("File location:", output_file)

    except Exception as error:

        print("Failed to generate financial dashboard:", error)

    finally:

        if cursor is not None:
            cursor.close()

        connection.close()
