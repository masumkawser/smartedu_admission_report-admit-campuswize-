import time
from odoo import models, fields, _
from odoo.exceptions import ValidationError
from odoo.http import request


class ProgramAndCampusWiseList(models.TransientModel):
    """ Admission Analysis Wizard """
    _name = "program.campus.wise.list"
    _description = "Program And Campus Wise Student Wizard"

    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'),
         ('confirm', 'Confirmed'), ('admission', 'Admission Confirm'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', default='draft', track_visibility='onchange')
    program_id = fields.Many2one('se.program', 'Course', required=True)
    campus_id = fields.Many2one(comodel_name='se.campus.facility', string="Campus", track_visibility='onchange')
    semester_id = fields.Many2one(comodel_name='se.semester', string="Semester", store=True, domain=[('is_active','=',True)], track_visibility='onchange')
    semester_year_string = fields.Char(string='Year')

    def check_report(self):
        semester_id = self.semester_id
        campus_id = self.campus_id
        semester_year_string = self.semester_year_string
        program_id = self.program_id
        state = self.state

        filter_report = [('semester_id', '=', semester_id.name), ('semester_year_string', '=', semester_year_string), ('program_id', '=', program_id.name)]

        # if self.state != 'done':
        #     filter_report.append(
        #         ('done', '=', self.state)
        #     )

        all_program_campus = request.env['se.application'].sudo().search(filter_report)

        all_report = []
        for program in all_program_campus:
            report = {
                'student_name': program.name,
                'student_id': program.student_id_string,
                'state': program.state,
                'course_name': program.program_id.name,
                'shift': program.education_shift_id.name,
                'hsc_board_name': program.education_board_hsc_id.name,
                'o_level_board_name': program.education_board_o_level_id.name,
                'gender': program.gender,
                # 'faculty_name': program.faculty_id.name,
                'district': program.permanent_district_id,
                'nationality': program.nationality,
            }
            all_report.append(report)

        return self.env.ref('smartedu_admission_report_admit_campuswize.report_se_program_campus_wise_list') \
            .report_action(self, {'program': all_report,
                                  'semester_id': semester_id.name,
                                  'semester_type': semester_id.semester_type_id.name,
                                  'semester_year_string': semester_year_string,
                                  'campus_id': campus_id.name,
                                  'state': state}, config=False)
