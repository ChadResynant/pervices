# Acode File Output Location

**Date:** November 21, 2025
**Source:** ResynantOVJ/src/nvpsg/AcodeBuffer.cpp:226-251

## Summary

The PSG compiler writes binary Acode files to specific paths in the acquisition queue directory. The bridge layer needs to intercept these files after PSG compilation completes.

## File Path Format

**Pattern:** `{goid}.{acodeStage}.{controllerName}`

**Example:** `/vnmrsystem/acqqueue/exp1.greg.012345.ps.Master1`

### Path Components

1. **`goid`** (Base Path)
   - VnmrJ parameter containing the acquisition queue path
   - Format: `/vnmrsystem/acqqueue/exp{N}.{user}.{timestamp}`
   - Example: `/vnmrsystem/acqqueue/exp1.greg.012345`
   - Retrieved via: `P_getstring(CURRENT,"goid",infopath,1,255)`

2. **`acodeStage`** (Compilation Stage)
   - Current stage name during multi-stage compilation
   - Common values: `ps` (pulse sequence)
   - Set by `AcodeManager` during compilation

3. **`controllerName`** (Hardware Controller)
   - Name of the controller generating this Acode stream
   - Examples: `Master1`, `RF1`, `RF2`, `PFG1`, `DDR1`
   - Each controller writes a separate Acode file

## Source Code Analysis

### File Creation (AcodeBuffer.cpp:226-251)

```cpp
int AcodeBuffer::openAcodeFile(int option)
{
  char buffer[200], infopath[256];

  // Get base path from goid parameter
  if (P_getstring(CURRENT,"goid",infopath,1,255) < 0)
     abort_message("psg internal acode buffer unable to get goid for %s. abort!\n",acodeName);

  if (checkflag)
  {
     // Dry-run mode: write to /dev/null
     ofs.open("/dev/null",ios::out|ios::binary);
  }
  else
  {
     // Construct Acode file path
     sprintf(buffer,"%s.%s.%s",infopath,acodeStage,acodeName);
     ofs.open(buffer,ios::out|ios::binary);
  }

  if ( ! ofs.is_open() )
  {
     if (bgflag) { cout << "AcodeBuffer:: acode buffer open FAILED for " << buffer << endl; }
     abort_message("psg internal acode buffer unable to open file for %s. abort!\n",acodeName);
  }

  if (bgflag)  { cout << "AcodeBuffer:: opened Acode file "<< buffer << endl; }
  return(acodeUniqueID);
}
```

### File Writing (AcodeBuffer.cpp:254-279)

```cpp
int AcodeBuffer::closeAcodeFile(int option)
{
  if (realWriteFlag)
  {
    openAcodeFile(option);      // Opens file for writing
    writeIncrement(option);     // Writes Acode binary data
    if ( ofs.is_open() )
    {
      ofs.close();             // Closes file
      return(0);
    }
    else
    {
      text_message("psg internal acode buffer output file stream is null for %s\n",acodeName);
      if (bgflag) { cout << " #### AcodeBuffer:: ERROR: ofs is NULL ! " << endl; }
      return(3);
    }
  }
  else
  {
    if (bgflag)
      cout << " #### WARNING: AcodeBuffer for " << acodeName << " is empty. No file written\n";

    return(-1);
  }
}
```

## Multiple Acode Files Per Sequence

**Important:** A single pulse sequence generates **multiple Acode files**, one per hardware controller.

### Example: hX Pulse Sequence

For a 1H-13C HETCOR experiment with `goid=/vnmrsystem/acqqueue/exp1.greg.012345`:

```
/vnmrsystem/acqqueue/exp1.greg.012345.ps.Master1   # Master timing controller
/vnmrsystem/acqqueue/exp1.greg.012345.ps.RF1       # 1H RF channel
/vnmrsystem/acqqueue/exp1.greg.012345.ps.RF2       # 13C RF channel
/vnmrsystem/acqqueue/exp1.greg.012345.ps.PFG1      # Pulsed field gradients (if used)
```

**Bridge Implication:** The bridge must read **all** Acode files for a sequence and coordinate execution across multiple Crimson TNG channels.

## Bridge Integration Strategy

### 1. Intercept PSG Completion

The bridge needs to detect when PSG compilation completes. Two approaches:

**Option A: Monitor for `psgdone` file**
- PSG writes completion flag to `{curexp}/psgdone` (see psgmain.cpp:1945-1947)
- Bridge watches this file via inotify or polling
- Once detected, read all Acode files matching `{goid}.ps.*`

**Option B: Replace `Sendproc` binary**
- OpenVNMRJ workflow: PSG → Acode files → Sendproc → Hardware
- Replace Sendproc with bridge that intercepts Acode files
- Bridge becomes the new "hardware interface"

**Recommended:** Option A (monitor `psgdone`) for clean separation and easier debugging.

### 2. Locate Acode Files

**Python Implementation:**
```python
import os
import glob

def get_acode_files(curexp: str) -> List[str]:
    """
    Get all Acode files for current experiment.

    Args:
        curexp: Current experiment directory (e.g., "/vnmr/exp1")

    Returns:
        List of Acode file paths
    """
    # Read goid from parameters
    goid = read_vnmrj_parameter(curexp, "goid")

    # Find all .ps.* Acode files
    acode_pattern = f"{goid}.ps.*"
    acode_files = glob.glob(acode_pattern)

    return sorted(acode_files)
```

### 3. Parse Multiple Acode Streams

**Architecture:**
```python
class AcodeBridge:
    def __init__(self, crimson_api):
        self.crimson_api = crimson_api
        self.parsers = {}  # {controller_name: AcodeParser}

    def load_sequence(self, curexp: str):
        """Load all Acode files for sequence."""
        acode_files = get_acode_files(curexp)

        for filepath in acode_files:
            # Extract controller name from filename
            # e.g., "exp1.greg.012345.ps.RF1" → "RF1"
            controller = os.path.basename(filepath).split('.')[-1]

            # Create parser for this controller
            parser = AcodeParser(filepath)
            self.parsers[controller] = parser

    def execute(self):
        """Execute synchronized multi-channel sequence."""
        # Parse all Acode streams
        sequences = {}
        for controller, parser in self.parsers.items():
            sequences[controller] = parser.parse()

        # Coordinate execution across Crimson TNG channels
        self.crimson_api.execute_multi_channel(sequences)
```

## Next Steps for Bridge Implementation

### Immediate (Today)

1. ✅ **Locate Acode files** (DONE - documented here)
2. **Test with real sequence:**
   - Compile `s2pul` in OpenVNMRJ
   - Locate generated Acode files
   - Hexdump first 1KB to validate binary format

### Short-term (This Week)

3. **Validate Acode parser:**
   - Read real Acode file with `acode_parser.py`
   - Verify opcode identification
   - Correlate with `acodes.h` definitions

4. **Implement multi-file parser:**
   - Extend `acode_parser.py` to handle multiple controllers
   - Synchronize timing across channels

### Medium-term (Next Week)

5. **Create bridge daemon:**
   - Watch `{curexp}/psgdone` for PSG completion
   - Auto-load and parse Acode files
   - Translate to Crimson TNG commands

## File Locations Reference

| Component | Path | Description |
|-----------|------|-------------|
| Base queue dir | `/vnmrsystem/acqqueue/` | All acquisition files |
| Experiment dir | `/vnmr/exp{N}/` | Current experiment parameters |
| PSG done flag | `/vnmr/exp{N}/psgdone` | Signals PSG completion |
| Acode files | `/vnmrsystem/acqqueue/{goid}.ps.*` | Binary pulse sequence code |
| Parameters | `/vnmr/exp{N}/curpar` | Experiment parameters |

## Critical Parameters

Read these VnmrJ parameters to locate files:

```python
curexp = read_parameter("CURRENT", "curexp")      # e.g., "/vnmr/exp1"
goid = read_parameter("CURRENT", "goid")          # e.g., "/vnmrsystem/acqqueue/exp1.greg.012345"
systemdir = read_parameter("GLOBAL", "systemdir") # e.g., "/vnmrsystem"
```

## Summary

The PSG compiler writes binary Acode files to:
- **Path format:** `{goid}.{stage}.{controller}`
- **Location:** `/vnmrsystem/acqqueue/exp{N}.{user}.{timestamp}.ps.{controller}`
- **Multiple files:** One per hardware controller (Master1, RF1, RF2, etc.)
- **Interception point:** Monitor `{curexp}/psgdone` file for completion signal

The bridge layer can now locate and parse these files to translate OpenVNMRJ pulse sequences into Crimson TNG commands.

---

*Analysis Date: November 21, 2025*
*Source Code: ResynantOVJ/src/nvpsg/AcodeBuffer.cpp*
*Related: PSG_ACODE_ANALYSIS.md, OVJ_CRIMSON_INTEGRATION_ARCHITECTURE.md*
