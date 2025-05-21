from datetime import datetime, date, time

# code modified from this promt and example (at the end of the file) 
# prompt: I’m building a Houdini tool with a UI where users select a start date, end date and frequency ("weekly" or "monthly").
# The frequency defines how date ranges are split:
# Weekly: fixed ranges of 01–07, 08–14, 15–21, and 22–28 each month.
# Monthly: 01–28 for each month.
# The function should round the start date down and the end date up to these intervals.
# In my PyQt UI, the widgets are named start_date, end_date, and weekly_monthly (with "weekly" and "monthly" as options).
# The output date ranges must be formatted like this (ISO 8601 with start at 00:00:00Z and end at 23:59:59Z):
# date_ranges = [
#     ("2018-08-01T00:00:00Z", "2018-08-07T23:59:59Z"),
#     ("2018-08-08T00:00:00Z", "2018-08-14T23:59:59Z"),
#     ("2018-08-15T00:00:00Z", "2018-08-21T23:59:59Z"),
#     ("2018-08-22T00:00:00Z", "2018-08-28T23:59:59Z"),
# ]

# THE CODE SUGGESTED BY COPILOT IS AT THE END OF THIS FILE!

def get_date_ranges(start_qdate, end_qdate, freq_text):
    """
    Generate date ranges based on start and end QDate objects and frequency.
    
    Args:
        start_qdate (QDate): Start date.
        end_qdate (QDate): End date.
        freq_text (str): Frequency type, either "weekly" or "monthly".

    Returns:
        ranges (list): List of tuples with ISO formatted date ranges.
    """
    # convert and clamp
    start = date(start_qdate.year(), start_qdate.month(), start_qdate.day())
    end   = date(end_qdate.year(),   end_qdate.month(),   end_qdate.day())
    
    def clamp28(d):
        return date(d.year, d.month, min(d.day, 28))
    
    start, end = clamp28(start), clamp28(end)

    # formatting utility
    def iso_range(d0, d1):
        return (
            datetime.combine(d0, time.min).strftime("%Y-%m-%dT%H:%M:%SZ"),
            datetime.combine(d1, time.max).strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    # iterate months
    def month_iter(d1, d2):
        y1, m1 = d1.year, d1.month
        y2, m2 = d2.year, d2.month
        y, m = y1, m1
        while (y, m) <= (y2, m2):
            yield y, m
            m += 1
            if m > 12:
                m, y = 1, y + 1

    ranges = []
    if freq_text.lower() == "weekly":
        segments = [(1,7), (8,14), (15,21), (22,28)]
        for yr, mth in month_iter(start, end):
            for ds, de in segments:
                seg_start = date(yr, mth, ds)
                seg_end   = date(yr, mth, de)
                if seg_end < start or seg_start > end:
                    continue
                # _always_ give the full week slice
                ranges.append(iso_range(seg_start, seg_end))

    elif freq_text.lower() == "monthly":
        for yr, mth in month_iter(start, end):
            seg_start = date(yr, mth, 1)
            seg_end   = date(yr, mth, 28)
            if seg_end < start or seg_start > end:
                continue
            ranges.append(iso_range(seg_start, seg_end))

    else:
        raise ValueError("freq_text must be 'weekly' or 'monthly'")

    return ranges


# CO-PILOT SUGGESTED THE FOLLOWING CODE:
# from datetime import datetime, date, time, timedelta
# import calendar

# def get_date_ranges(start_qdate, end_qdate, freq_text):
#     """
#     start_qdate, end_qdate: QDate objects from your UI
#     freq_text: "weekly" or "monthly"
#     """
#     # Convert to Python dates
#     start = start_qdate.toPyDate()
#     end   = end_qdate.toPyDate()
    
#     # Helper to ISO-format with full-day coverage
#     def iso_range(d0, d1):
#         # d0 at 00:00, d1 at 23:59:59
#         start_iso = datetime.combine(d0, time.min).strftime("%Y-%m-%dT%H:%M:%SZ")
#         end_iso   = datetime.combine(d1, time.max).strftime("%Y-%m-%dT%H:%M:%SZ")
#         return start_iso, end_iso

#     ranges = []

#     # Generate all months between start and end (inclusive)
#     def month_iter(d1, d2):
#         ym1 = (d1.year, d1.month)
#         ym2 = (d2.year, d2.month)
#         year, month = ym1
#         while (year, month) <= ym2:
#             yield year, month
#             month += 1
#             if month > 12:
#                 month = 1
#                 year += 1

#     if freq_text.lower() == "weekly":
#         # Define the four weekly segments in any month
#         week_segments = [
#             (1, 7),
#             (8, 14),
#             (15, 21),
#             (22, 28),
#         ]
#         for yr, mth in month_iter(start, end):
#             for day_start, day_end in week_segments:
#                 seg_start = date(yr, mth, day_start)
#                 seg_end   = date(yr, mth, day_end)
#                 # Skip segments completely outside the overall window
#                 if seg_end < start or seg_start > end:
#                     continue
#                 # Clip to the overall start/end
#                 real_start = max(seg_start, start)
#                 real_end   = min(seg_end,   end)
#                 ranges.append(iso_range(real_start, real_end))

#     elif freq_text.lower() == "monthly":
#         # One segment per month, always 1st → 28th
#         for yr, mth in month_iter(start, end):
#             seg_start = date(yr, mth, 1)
#             seg_end   = date(yr, mth, 28)
#             if seg_end < start or seg_start > end:
#                 continue
#             real_start = max(seg_start, start)
#             real_end   = min(seg_end,   end)
#             ranges.append(iso_range(real_start, real_end))

#     else:
#         raise ValueError("freq_text must be 'weekly' or 'monthly'")

#     return ranges


# # ——— Example of wiring it up in your MainWindow class ———

# # somewhere in your slot or on “Apply” button click:
# def on_apply(self):
#     start_qdate = self.start_date.date()
#     end_qdate   = self.end_date.date()
#     freq_text   = self.weekly_monthly.currentText()  # "weekly" or "monthly"

#     date_ranges = get_date_ranges(start_qdate, end_qdate, freq_text)
#     # date_ranges is now a list of ("YYYY-MM-DDT00:00:00Z","YYYY-MM-DD-23:59:59Z") tuples
#     print(date_ranges)
#     # …feed date_ranges into the rest of your pipeline…
