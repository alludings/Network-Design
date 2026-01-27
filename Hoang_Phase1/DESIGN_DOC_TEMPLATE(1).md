# Network Design Project – Phase Proposal & Design Document (Phase __ of 5)

> **Purpose:** This document is your team’s *proposal* for how you will implement the current phase **before** you start coding.  
> Keep it clear, concrete, and lightweight.

**Team Name:**  NHT
**Members:** Nathan Hoang, Nathan_Hoang@student.uml.edu
**GitHub Repo URL (with GitHub usernames):**  https://github.com/alludings/Network-Design (alludings)

**Phase:** 1  
**Submission Date:**  1/27/26
**Version:** resubmission v2 

---

## 0) Executive summary
Within this phase, socket programming is the primary target of expertise, transferring data on UDP communication written in Python. In Phase 1(a), an algorithm is developed that will repeat a simple message that is written by the user, essentially an echo. Phase 1(b) is a continuation where, instead of a message, it is a BMP file being transferred using the RDT 1.0 protocol. The algorithms will be validated through edge cases that are stated further, mostly ensuring that the system follows through even in unique cases. It will also be shown through a live demo, where the transferred file will be a replica of the input file.

## 1) Phase requirements
### 1.1 Demo deliverable
You will submit a **screen recording** demonstrating the required scenarios.

- **Private YouTube link:** *(fill in at submission time)*  
  - Link:
  - Timestamped outline (mm:ss → scenario name):

### 1.2 Required demo scenarios
Fill in the scenarios required by the phase spec.

| Scenario | What you will inject / configure | Expected observable behavior | What we will see in the video |
|---|---|---|---|
| 1 | Change the message text instead of HELLO | Server correctly receives the modified message and echoes it back | Video shows bidirectional message exchange |
| 2 | Transfer a larger BMP file | RDT1.0 continues correctly | The video shows a continuous file transfer |
| 3 | Verify output integrity | Start and end file match properly | Side-by-side comparison between the two files |

### 1.3 Required figures / plots
Fill in the figures/plots required by the phase spec (if none, write “N/A”).

| Figure/Plot | X-axis | Y-axis | Sweep range + step | Data source (CSV/log) | Output filename |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |

--- N/A

## 2) Phase plan (company-style, lightweight)
Think of this as a short “implementation proposal” you’d write at a company.

### 2.1 Scope: what changes/additions this phase
- **New behaviors added:**
- **Behaviors unchanged from previous phase:**
- **Out of scope (explicitly):**
New behaviors:
- UDP-based client and server socket communication
- Message exchange over UDP
- Reassemble received packets to reconstruct the file
Behaviors unchanged:
- This is the first phase, so everything will be new and independent of any previous work done. 
Out of scope:
- Packet loss
- Packet corruption
- Optimized performance


### 2.2 Acceptance criteria (your checklist)
List 5–10 measurable checks that mean you’re done (examples below).

- UDP message exchange between hellos works properly
- File transfer over UDP using RDT1.0 completes
- Received file matches original file
- Program runs 
- The program can repeat itself


### 2.3 Work breakdown (high-level; Person X will work on A, Person Y will work on B...)
- Workstream A: Nathan
- Workstream B: Nathan
- Workstream C: Nathan

---

## 3) Architecture + state diagrams
Your phase specs likely include a reference state diagram. **You should build on it across phases.**

### 3.1 How to evolve the provided state diagram
For each phase:
1. **Start from the current phase diagram** (sender + receiver).
2. **Mark specifics**:
   - new states,
   - new transitions,
   - updated transition conditions (timeouts, corruption checks, window slide rules).
3. Keep both:
   - **“Previous phase diagram”** (for comparison) and
   - **“Current phase diagram”** (what you will implement in more detail).

> Tip: In your PDF submission, include diagrams as images. In Markdown, you can include ASCII diagrams or link to images in `docs/figures/`.

https://docs.google.com/document/d/1F4i15UEzsjFcHOhNzu28AXyCBdW2fhKG4kXX7E4bIVk/edit?usp=sharing
First phase, no new implementations

### 3.2 Component responsibilities
- **Sender**
  - responsibilities:
    - read input file
    - Segment the file into data chunks and put them into UDP packets
    - Sends packets to the receiver
- **Receiver**
  - responsibilities:
    - Waits for UDP packets
    - Receive and decode said packets
    - Write the deconstruction data into the output file
    - Log packet replication
- **Shared modules/utilities**
  - packet encode/decode:
    - Define RDT packet format
    - Serialize packet structures for transfer
    - Deserialize packets into header and payload fields
  - checksum:
    - Compute the checksum on packets
  - logging/timing:
    - Record events and timestamps
  - CLI/config parsing:
    - Validate inputs and provide instructions

### 3.3 Message flow overview
Add a simple diagram (box + arrows is fine, you're also welcome to use software with screenshots).

Example:
```
[file] -> Sender -> UDP -> Receiver -> [output file]
              ^             |
              |---- ACK ----|
```

---
https://docs.google.com/document/d/1F4i15UEzsjFcHOhNzu28AXyCBdW2fhKG4kXX7E4bIVk/edit?usp=sharing

## 4) Packet format (high-level spec)
Define your on-the-wire format **unambiguously**.

### 4.1 Packet types
List the packet types you will send:
- Data packet - carries file data from sender to receiver
- End of transfer packet - signals completion of transfer

### 4.2 Header fields (this is the “field table”)
**What this means:** you must specify the *exact* fields in each packet header and their meaning.  
This ensures everyone can encode/decode packets consistently.

| Field | Size (bytes/bits) | Type | Description | Notes |
|---|---:|---|---|---|
| type | 1b | uint8 | data vs ack |  |
| seq | 1b | uint8 | sequence number |  |
| ack | 1b | uint8 | ack number / flag |  |
| len | 2b | uint16 | payload length | last packet may be smaller |
| checksum | 2b | uint16 | checksum value | what it covers (header/payload) |
| payload | ≤ ~1024B | bytes | file chunk | binary-safe |

---

## 5) Data structures + module map
This section prevents “random globals everywhere” and helps keep code maintainable.

### 5.1 Key data structures
List the core structures you will store in memory.

Sender Packet - loc. src/packet.*
Receiver Packet - loc. src/packet.*
File buffer - loc. src/sender.* and src/receiver.*
Logging - loc.src/utils.*

### 5.2 Module map + dependencies
Show how modules connect.

Minimum expected modules (names may vary):
- `src/sender.*`
- `src/receiver.*`
- `src/packet.*` (encode/decode)
- `src/checksum.*`
- `scripts/run_experiments.*` (if applicable)
- `scripts/plot_results.*` (if applicable)

Provide a simple dependency sketch:

```
sender -> packet, checksum, utils
receiver -> packet, checksum, utils
packet -> checksum
checksum -> utils
scripts -> sender/receiver CLI, results CSV, plotting
```
---

## 6) Protocol logic (high-level spec before implementation)
This section is your “engineering spec” that you implement against. Keep it precise but not code-heavy.

### 6.1 Sender behavior
Describe behavior as steps or a state machine:
Sender behavior
- Read a chunk of data from the input
- Create a packet using make data
- Compute checksum
- Send packet to receiver 
- Repeat until transfer is complete

**Sender pseudocode (recommended):**
```text
initialize state
while not done:
  send/queue packets according to phase rules
  wait for ACK/event
  if ACK received:
    validate (checksum/seq)
    update state (advance, ignore duplicate, etc.)
  if timeout/event:
    retransmit according to phase rules
```

### 6.2 Receiver behavior
Describe receiver rules:
Receiver behavior
- Decode the given packet from the sender
- Check checksum
- Extract payload and apply to the output file
- Close the output file

**Receiver pseudocode (recommended):**
```text
on packet receive:
  if corrupt: discard; respond according to phase rules
  else if expected: accept; write/buffer; ACK
  else: handle duplicate/out-of-order according to phase rules
```

### 6.3 Error/loss injection spec (if required by phase)
If the phase requires injection, state:
- where injection occurs in the pipeline (exact point)
- probability model and RNG seed usage
- what is injected (bit flip vs drop)
- how you ensure repeatability

--- N/A

## 7) Experiments + metrics plan (required if phase requires figures/plots)
### 7.1 Measurement definition
Define completion time precisely:
- start moment: When transmitter receives the first packet over UDP
- stop moment: Receiver processes the end fo transfer packet

State how you will avoid measurement distortion:
- disable verbose printing/logging during timing runs
- run multiple trials if required

### 7.2 Output artifacts
- CSV schema (columns): N/A
- plot filenames: N/A
- where outputs are stored (`results/`): log

---

## 8) Edge cases + test plan
This replaces “risks” with what actually matters for correctness.

### 8.1 Edge cases you expect
List the top edge cases you will explicitly test.

| Edge case | Why it matters | Expected behavior |
|---|---|---|
| last packet smaller than payload size | correct file reconstruction | receiver writes exact bytes |
| duplicate packets/ACKs | protocol correctness | ignored or re-ACKed |
| corrupted header | checksum coverage | drop / request retransmit |
| termination marker handling | clean shutdown | no deadlocks |

### 8.2 Tests you will write because of these edge cases
List concrete tests (unit/integration) that map to the edge cases.

- Unit tests (examples):
  - checksum correctness on known inputs
  - packet encode/decode round-trip
  - packet length handling
- Integration tests (examples):
  - send file and verify output hash matches input
  - run scenario injection and confirm behavior
  - send a 0 byte file and verify that receiver exits properly

### 8.3 Test artifacts
State what artifacts you will produce:
- console logs (minimal)
- where tests live (`tests/` optional, or `scripts/`)
Unit tests: tests/unit/
Integration tests: tests/integration/

---


## 9) Repo structure + reproducibility
Your repo must contain at minimum:

```
src/
scripts/
docs/
results/
README.md
```

State where phase artifacts live:
- Design docs: `docs/`
- Figures/plots + CSV: `results/`
- Any helper scripts: `scripts/`

---

## 10) Team plan, ownership, and milestones
### 10.1 Task ownership
| Task | Owner | Target date | Definition of done |
|---|---|---|---|
| Packet format + encode/decode |  |  |  |
| Sender logic |  |  |  |
| Receiver logic |  |  |  |
| Injection (if required) |  |  |  |
| Figures/plots (if required) |  |  |  |
| README + reproducibility |  |  |  |

### 10.2 Milestones (keep it realistic)
- Milestone 1:
- Milestone 2:
- Milestone 3:

---

## Appendix (optional)
