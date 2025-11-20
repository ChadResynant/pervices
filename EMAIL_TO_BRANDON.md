# Email to Brandon Malatest - Ready to Send

**To:** brandon.m@pervices.com
**CC:** laura.m@pervices.com
**Subject:** Resynant NMR Project - Technical Documentation and Next Steps

---

Hi Brandon,

Thank you for your patience over the past few weeks. I apologize for the delay in getting back to you - we've had some exciting developments that I wanted to finalize before moving forward.

**POSITIVE UPDATES:**
1. **Funding Secured:** We've received a $900K purchase order from Indiana University and are closing our Series A financing ($1M) this week, giving us strong financial backing for this development program.

2. **Team Assigned:** I've dedicated Lauren Price as Assistant Project Manager and Alex Dreena (Head of R&D) as full-time Lab Technician. I will personally serve as NMR Specialist and Software Engineer, committing 20+ hours/week during the critical development phase.

3. **Resources Ready:** We have 400 MHz and 600 MHz NMR magnets available 24/7 for testing, all required test equipment in-house, and test samples prepared.

4. **Beta Test Opportunity:** Indiana University will receive a prototype console in March 2026, providing an excellent beta test site for the Per Vices Crimson TNG integration.

**REVISED TIMELINE:**
Given our preparation work, I'm proposing a realistic timeline:
- **Statement of Work Approval:** December 13, 2025
- **Prototype Delivery:** February 28, 2026
- **Validation Complete:** May 15, 2026
- **Beta Testing at Indiana:** May-June 2026
- **Production Release:** August 1, 2026

**TECHNICAL DOCUMENTATION:**
I'm attaching comprehensive technical specifications (~4,500 lines across 7 documents):

1. **executive_summary.md** - Business context and project overview
2. **technical_requirements.md** - Detailed system specifications
3. **requirements_summary.md** - Requirements traceability and gap analysis
4. **use_case_scenarios.md** - NMR operational scenarios
5. **test_validation_plan.md** - Validation procedures and acceptance criteria
6. **nmr_pulse_sequences.md** - FPGA waveform requirements
7. **GPIO_SPECIFICATIONS.md** - TTL trigger interface requirements (NEW - see below)

**CRITICAL REQUIREMENT - GPIO TTL INTERFACE:**
I've created a detailed GPIO specification (attached separately for easy reference). The key requirement is:

- **Minimum:** 2 TTL outputs per channel (8 total) - TX enable, RX enable
- **Preferred:** 3 per channel (12 total) - adds 1 spare for prototyping
- **Ultimate:** 4 per channel (16 total) - adds flexibility for future needs
- **Specifications:** 0-5V TTL, ~100ns timing precision, FPGA-controlled

Please review the GPIO_SPECIFICATIONS.md document and let me know if this is achievable with your GPIO expander approach.

**IMMEDIATE NEXT STEPS:**
1. **Technical Review (This Week):** Please have your engineering team review the attached documentation and provide feedback on:
   - GPIO expander feasibility and specifications
   - FPGA CIC decimation implementation status and NRE estimate
   - Confirmed frequency range coverage (20-1400 MHz)
   - Any concerns or clarifications needed

2. **Technical Alignment Call (Week of Nov 25):** I'd like to schedule a 60-minute technical discussion with your lead engineer to review:
   - GPIO interface approach
   - FPGA development scope and timeline
   - Dynamic range validation methodology
   - SOW content and deliverables

3. **SOW Draft (Week of Dec 2):** Target delivery of draft SOW by December 6 for internal review, with approval by December 13.

**REQUEST FOR INFORMATION:**
Could you please send me:
- PVAN-11 data format specification (link: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/)
- Any additional Crimson TNG API documentation for software development
- Preliminary NRE estimate for FPGA customization (GPIO + CIC decimation)

**AVAILABILITY FOR CALL:**
I'm available next week for a technical discussion:
- Monday, Nov 25: 10am-4pm Central
- Tuesday, Nov 26: 9am-3pm Central
- Wednesday, Nov 27: 10am-2pm Central (before Thanksgiving)

Please let me know what works best for your team.

I'm excited to move this project forward. Per Vices has been excellent to work with, and the Crimson TNG is an outstanding fit for our NMR application. With our funding secured and team dedicated, we're ready to execute on this development program.

Looking forward to your response and to working together on this exciting project.

Best regards,

Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
(217) 649-8932

---

**ATTACHMENTS:**
- executive_summary.md
- technical_requirements.md
- requirements_summary.md
- use_case_scenarios.md
- test_validation_plan.md
- nmr_pulse_sequences.md
- GPIO_SPECIFICATIONS.md (NEW)
- REVISED_PROJECT_TIMELINE.md (NEW)
