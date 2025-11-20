# 4-DAY SPRINT IMPLEMENTATION GUIDE
## November 21-24, 2025
### Get the Resynant-Per Vices NMR Project Back on Track

**Sprint Goal:** Break through the execution blocker and re-engage Per Vices with complete documentation package

**Team:** Chad Rienstra (lead), Lauren Price (PM support), Alex Dreena (R&D support)

---

## ✅ COMPLETED (Nov 21 Morning)

**Documents Created and Ready:**
1. ✅ **EMAIL_TO_BRANDON.md** - Professional re-engagement email with positive updates
2. ✅ **GPIO_SPECIFICATIONS.md** - Complete GPIO TTL interface requirements (7 pages)
3. ✅ **REVISED_PROJECT_TIMELINE.md** - Realistic 36-week timeline to Aug 2026 production

**Status:** Ready to send to Per Vices TODAY

---

## 🎯 THURSDAY NOV 21 (REMAINING TASKS) - 4-6 hours

### Task 1: Send Email to Brandon Malatest (30 minutes) ⚠️ HIGHEST PRIORITY
**Action Items:**
1. Review EMAIL_TO_BRANDON.md one more time
2. Copy email text into your email client
3. Attach the following files:
   - executive_summary.md
   - technical_requirements.md
   - requirements_summary.md
   - use_case_scenarios.md
   - test_validation_plan.md
   - nmr_pulse_sequences.md
   - GPIO_SPECIFICATIONS.md
   - REVISED_PROJECT_TIMELINE.md
4. Send to: brandon.m@pervices.com
5. CC: laura.m@pervices.com
6. **SEND BEFORE END OF DAY THURSDAY**

**Why This Matters:** This breaks the 5-week communication logjam with Per Vices. Brandon has been patient and responsive - he'll appreciate the comprehensive package.

---

### Task 2: Download PVAN-11 Data Format Specification (15 minutes)
**Action Items:**
1. Visit: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/
2. Download and save PVAN-11 specification document
3. Read through quickly (detailed study tomorrow)
4. Identify key sections: UDP packet format, I/Q data structure, metadata

**Deliverable:** PVAN-11 spec saved locally, quick overview complete

---

### Task 3: Set Up Development Environment (2 hours)
**Choose Your Language:** Python (recommended for prototyping) or C++ (for performance)

**If Python:**
```bash
# Create virtual environment
python3 -m venv pervices-nmr-env
source pervices-nmr-env/bin/activate

# Install required libraries
pip install numpy scipy matplotlib
pip install asyncio  # For async UDP reception

# Create project structure
mkdir -p pervices-nmr-software/{src,tests,docs,data}
cd pervices-nmr-software
git init
```

**If C++:**
```bash
# Install required libraries
sudo apt-get install libboost-all-dev libfftw3-dev

# Create project structure
mkdir -p pervices-nmr-software/{src,include,tests,build}
cd pervices-nmr-software
git init

# Create CMakeLists.txt (basic template)
```

**Action Items:**
1. Choose language (Python recommended for sprint)
2. Install libraries and dependencies
3. Create project directory structure
4. Initialize git repository
5. Create README.md with project description

**Deliverable:** Development environment ready for coding

---

### Task 4: Create UDP Receiver Skeleton Code (2 hours)
**Goal:** Basic structure for receiving UDP packets from Crimson TNG

**Python Example:**
```python
# udp_receiver.py
import socket
import struct
import numpy as np

class PerVicesUDPReceiver:
    def __init__(self, ip='0.0.0.0', port=28888):
        self.ip = ip
        self.port = port
        self.socket = None

    def start(self):
        """Initialize UDP socket"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        print(f"UDP receiver listening on {self.ip}:{self.port}")

    def receive_packet(self):
        """Receive single UDP packet"""
        data, addr = self.socket.recvfrom(65536)  # Max UDP packet size
        return self.parse_packet(data)

    def parse_packet(self, data):
        """Parse PVAN-11 packet format (TO BE IMPLEMENTED)"""
        # TODO: Implement based on PVAN-11 spec
        pass

    def stop(self):
        """Close socket"""
        if self.socket:
            self.socket.close()

# Test harness
if __name__ == '__main__':
    receiver = PerVicesUDPReceiver()
    receiver.start()
    print("Waiting for packets... (Ctrl+C to stop)")
    try:
        while True:
            packet = receiver.receive_packet()
            # Process packet
    except KeyboardInterrupt:
        print("\nStopping receiver")
        receiver.stop()
```

**Action Items:**
1. Create udp_receiver.py with basic structure
2. Test socket creation and binding
3. Create placeholder for PVAN-11 packet parsing
4. Test with simple UDP packet generator (if time permits)

**Deliverable:** UDP receiver skeleton code, ready for PVAN-11 implementation tomorrow

---

### Task 5: Brief Lauren and Alex (30 minutes)
**Meeting Agenda:**
1. Project status update (5 min)
   - Email going to Per Vices today
   - Revised timeline: Production Aug 2026 (not June)
   - Sprint plan: Nov 21-24

2. Role assignments (10 min)
   - Lauren: Project Manager, liaison with Per Vices
   - Alex: Lab setup, test equipment preparation
   - Chad: NMR specialist + software development

3. Immediate tasks (10 min)
   - Lauren: Review EMAIL_TO_BRANDON.md, prepare for Per Vices call next week
   - Alex: Inventory test equipment, prepare lab for Feb validation
   - Chad: Software development sprint (this weekend)

4. Next week plan (5 min)
   - Monday/Tuesday: Technical call with Per Vices
   - Review Per Vices feedback on documentation
   - Prepare for SOW review (target Dec 6)

**Deliverable:** Team aligned and ready for sprint execution

---

## 📅 FRIDAY NOV 22 - 6 hours

### Task 6: Study PVAN-11 Specification (2 hours)
**Action Items:**
1. Read PVAN-11 spec in detail
2. Understand UDP packet structure:
   - Header format
   - I/Q data encoding (16-bit samples)
   - Channel identification
   - Timestamp/sequence number
3. Document key findings in notes file
4. Identify any ambiguities or questions for Per Vices

**Deliverable:** Complete understanding of PVAN-11 format, notes prepared

---

### Task 7: Implement PVAN-11 Packet Parsing (3 hours)
**Action Items:**
1. Update udp_receiver.py with PVAN-11 parsing logic
2. Extract I/Q samples from packet
3. Handle channel identification
4. Implement timestamp tracking
5. Create data validation (checksum, sequence checks)

**Python Example:**
```python
def parse_pvan11_packet(self, data):
    """
    Parse PVAN-11 packet format
    Based on: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/
    """
    # Header parsing (adjust based on actual spec)
    header_size = 32  # Example, check actual spec
    header = struct.unpack('!IIIIIIII', data[:header_size])

    packet_id = header[0]
    channel_id = header[1]
    timestamp = header[2]
    sample_count = header[3]

    # I/Q data extraction
    payload = data[header_size:]
    samples = np.frombuffer(payload, dtype=np.int16)

    # Separate I and Q
    i_samples = samples[0::2]
    q_samples = samples[1::2]

    return {
        'packet_id': packet_id,
        'channel': channel_id,
        'timestamp': timestamp,
        'i_data': i_samples,
        'q_data': q_samples,
        'sample_count': len(i_samples)
    }
```

**Deliverable:** Working PVAN-11 packet parser, validated with test data

---

### Task 8: Create Test Harness (1 hour)
**Action Items:**
1. Create test_udp_receiver.py
2. Generate simulated PVAN-11 packets
3. Test packet reception and parsing
4. Validate I/Q data extraction
5. Test multi-channel handling (4 channels)

**Deliverable:** Tested UDP receiver with simulated data

---

## 🏃 WEEKEND NOV 23-24 - 8 hours total (4 hrs each day)

### Task 9: Data Buffering and Ring Buffer (3 hours)
**Goal:** Implement real-time data buffering for continuous acquisition

**Action Items:**
1. Create ring buffer class for continuous data storage
2. Implement buffer overflow handling
3. Create data export function (save to file)
4. Test with sustained data rate simulation

**Python Example:**
```python
class RingBuffer:
    def __init__(self, capacity=10000000):  # 10M samples
        self.capacity = capacity
        self.buffer_i = np.zeros(capacity, dtype=np.int16)
        self.buffer_q = np.zeros(capacity, dtype=np.int16)
        self.write_pos = 0
        self.read_pos = 0

    def write(self, i_samples, q_samples):
        """Write samples to buffer"""
        n_samples = len(i_samples)

        # Handle wraparound
        if self.write_pos + n_samples > self.capacity:
            # Split write
            first_chunk = self.capacity - self.write_pos
            self.buffer_i[self.write_pos:] = i_samples[:first_chunk]
            self.buffer_q[self.write_pos:] = q_samples[:first_chunk]

            remaining = n_samples - first_chunk
            self.buffer_i[:remaining] = i_samples[first_chunk:]
            self.buffer_q[:remaining] = q_samples[first_chunk:]

            self.write_pos = remaining
        else:
            self.buffer_i[self.write_pos:self.write_pos+n_samples] = i_samples
            self.buffer_q[self.write_pos:self.write_pos+n_samples] = q_samples
            self.write_pos += n_samples

    def read(self, n_samples):
        """Read samples from buffer"""
        # Implementation for data retrieval
        pass
```

**Deliverable:** Ring buffer implementation, tested with simulated data stream

---

### Task 10: Basic Signal Processing Pipeline (3 hours)
**Goal:** Convert I/Q samples to complex data, apply basic processing

**Action Items:**
1. Convert I/Q to complex samples (I + jQ)
2. Implement basic FIR filter (decimation)
3. Apply FFT for spectral view
4. Create data visualization (matplotlib)

**Python Example:**
```python
def process_iq_data(i_samples, q_samples):
    """
    Process I/Q data to FID (Free Induction Decay)
    """
    # Convert to complex
    complex_samples = i_samples.astype(np.float32) + 1j * q_samples.astype(np.float32)

    # Apply digital downconversion (if needed)
    # (Skip for now, assume already at baseband)

    # Decimation filter (example: downsample 32x)
    decimation_factor = 32
    fir_coefficients = signal.firwin(64, 1.0/decimation_factor)
    filtered = signal.lfilter(fir_coefficients, 1.0, complex_samples)
    decimated = filtered[::decimation_factor]

    return decimated

def compute_spectrum(fid_data):
    """
    Compute NMR spectrum via FFT
    """
    # Zero-fill for better resolution
    zf_size = len(fid_data) * 2
    fid_zf = np.zeros(zf_size, dtype=np.complex64)
    fid_zf[:len(fid_data)] = fid_data

    # Apply apodization (exponential window)
    lb = 50  # Line broadening in Hz
    time_axis = np.arange(len(fid_data)) / 100000  # Assuming 100 kHz SW
    apodization = np.exp(-lb * np.pi * time_axis)
    fid_apodized = fid_data * apodization

    # FFT
    spectrum = np.fft.fftshift(np.fft.fft(fid_zf))

    return np.abs(spectrum)
```

**Deliverable:** Signal processing pipeline, visualization of simulated NMR data

---

### Task 11: Indiana Deployment Planning (2 hours)
**Goal:** Define prototype vs. beta deployment plan for Indiana

**Action Items:**
1. Create deployment timeline for Indiana console
2. Define what goes in March prototype (legacy Varian-based)
3. Define what goes in May upgrade (Per Vices Crimson TNG)
4. Identify beta test objectives and success metrics
5. Draft communication plan for Indiana customer

**Document to Create:** INDIANA_DEPLOYMENT_PLAN.md

**Deliverable:** Clear plan for Indiana beta testing opportunity

---

## 📞 MONDAY NOV 25 - 2 hours

### Task 12: Technical Call with Per Vices (1 hour)
**Pre-Call Preparation:**
- Review EMAIL_TO_BRANDON.md and all attached documents
- Prepare list of questions based on their feedback
- Have GPIO_SPECIFICATIONS.md handy for detailed discussion
- Take notes on Per Vices responses

**Call Agenda (proposed):**
1. Introduction and project status (5 min)
2. Review technical documentation (10 min)
   - GPIO expander approach
   - FPGA CIC decimation status
   - Frequency range confirmation
3. SOW development timeline (10 min)
   - Target delivery: Dec 6
   - Key deliverables and milestones
   - NRE cost estimate
4. Technical questions and clarifications (20 min)
5. Next steps and action items (5 min)

**Deliverable:** Meeting notes, action items list, SOW timeline confirmed

---

### Task 13: Post-Call Follow-Up (1 hour)
**Action Items:**
1. Send thank-you email to Brandon
2. Summarize key takeaways and action items
3. Update project timeline if needed based on Per Vices feedback
4. Share notes with Lauren and Alex
5. Plan for SOW review (Dec 2-6)

**Deliverable:** Team aligned on Per Vices feedback, ready for SOW phase

---

## ✅ SPRINT SUCCESS CRITERIA

By end of Monday Nov 25, you will have:

1. ✅ **Re-engaged Per Vices** with complete documentation package sent
2. ✅ **Completed GPIO specifications** addressing their critical question
3. ✅ **Revised realistic timeline** eliminating decision paralysis
4. ✅ **Working UDP receiver** ready for PVAN-11 packet handling
5. ✅ **Signal processing pipeline** skeleton for NMR data
6. ✅ **Team aligned** (Lauren, Alex) on roles and next steps
7. ✅ **Technical call completed** with Per Vices (or scheduled)
8. ✅ **SOW timeline confirmed** targeting Dec 13 approval

---

## 🚧 POTENTIAL BLOCKERS & MITIGATION

### Blocker 1: "I'm too busy to code this weekend"
**Mitigation:**
- The email to Brandon (Task 1) is HIGHEST priority - everything else is bonus
- Even 2 hours on software this weekend is progress
- Consider delegating UDP receiver development to contractor ($2K-$5K for basic implementation)

### Blocker 2: "I don't know PVAN-11 format well enough yet"
**Mitigation:**
- Start with skeleton code (done!)
- Fill in details as you learn the spec
- Ask Per Vices for sample data or reference code
- It's OK to have incomplete implementation for first call

### Blocker 3: "Per Vices doesn't respond quickly"
**Mitigation:**
- Send email TODAY regardless
- Follow up with phone call if no response by Tuesday
- Brandon's number: +1 (647) 534-9007
- They've been very responsive historically - this is on us to send

### Blocker 4: "Other urgent projects come up"
**Mitigation:**
- Protect at least 2 hours per day Nov 21-24
- Email to Brandon is 30-minute task - do it FIRST thing
- Everything else can be compressed if needed
- Series A closing is huge win - use that momentum!

---

## 💡 DELEGATION OPPORTUNITIES

If you find yourself short on time, consider delegating:

### Can Delegate to Software Contractor:
- UDP receiver full implementation ($2K-$5K)
- PVAN-11 packet parsing and testing
- Ring buffer and data management
- Signal processing pipeline (FIR, FFT, visualization)
- **Estimated Cost:** $5K-$10K for full sprint implementation
- **Time Saved:** 8-12 hours of your time

### Lauren Can Handle:
- Scheduling Per Vices technical call
- Taking notes during Per Vices call
- Following up with Per Vices on action items
- Tracking project timeline and milestones

### Alex Can Handle:
- Test equipment inventory and preparation
- Lab space setup for prototype arrival (Feb)
- Test sample organization and documentation
- Indiana deployment logistics coordination

---

## 🎯 THE ONE THING THAT MATTERS MOST

**If you can only do ONE thing from this sprint:**

### → Send the email to Brandon Malatest TODAY

Everything else is secondary. The 5-week communication gap is the real blocker. Your documentation is excellent. Brandon has been patient and engaged. Just send the email.

**30 minutes. That's all it takes to unblock this project.**

---

## 📊 PROGRESS TRACKING

### Thursday Nov 21 End of Day:
- [ ] Email sent to Per Vices
- [ ] PVAN-11 spec downloaded
- [ ] Development environment set up
- [ ] UDP receiver skeleton created
- [ ] Team briefed (Lauren, Alex)

### Friday Nov 22 End of Day:
- [ ] PVAN-11 spec studied and documented
- [ ] Packet parsing implemented
- [ ] Test harness created
- [ ] Basic tests passing

### Weekend Nov 23-24:
- [ ] Ring buffer implemented
- [ ] Signal processing pipeline working
- [ ] Indiana deployment plan drafted
- [ ] Ready for Per Vices call Monday

### Monday Nov 25:
- [ ] Technical call with Per Vices completed
- [ ] SOW timeline confirmed (Dec 6 draft, Dec 13 approval)
- [ ] Team aligned on next steps
- [ ] **SPRINT SUCCESS! 🎉**

---

## 🚀 MOMENTUM BUILDERS

**You have incredible momentum right now:**
- ✅ $900K Indiana PO secured
- ✅ $1M Series A closing this week
- ✅ Team identified and committed (Lauren, Alex)
- ✅ All equipment and samples ready
- ✅ 4,500+ lines of excellent technical documentation
- ✅ Per Vices has been responsive and engaged

**Don't let perfectionism kill this momentum.**

Send the email. Make the call. Write the code.

**You've got this! 💪**

---

**Questions during sprint? Create issues in your notes and keep moving forward. Perfect is the enemy of done.**

**Good luck with your 4-day sprint! 🎯**
