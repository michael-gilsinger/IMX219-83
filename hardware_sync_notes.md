Hardware-triggered sync notes for IMX219-83 stereo rigs

Overview
- True per-frame hardware sync requires external trigger or matched sensor clocking and is preferable to software-only sync.
- Options vary by module/carrier board: external trigger pin, trigger-over-GPIO, or vendor stereo board with shared MCLK and sync lines.

Recommendations
- If your camera carrier supports a STROBE/VSYNC trigger input, use that as a master trigger to both sensors.
- Use a stereo adapter board that routes sensors to separate CSI ports but shares a common external trigger/MCLK when available.
- Some Arducam stereo HATs include hardware sync and provide kernel/device-tree overlays — prefer vendor-supplied overlays.

Driver/kernel notes
- Verify the imx219 driver in your L4T kernel supports external trigger lines. You may need to enable sensor-specific DT properties such as `gpio_fetch`, `camif_sync` or `external_clock`.
- If hardware sync isn't supported out-of-the-box, you can:
  - Use a small FPGA/MCU to fan-out an external trigger to the sensors' TRIG pins.
  - Modify driver/device-tree to expose and use the trigger GPIO.

Testing approach
1. With both cameras attached, run `v4l2-ctl --list-devices` and note `/dev/videoX` nodes.
2. Capture timestamped frames using `gst_capture.py` or `capture.py` and compare timestamps to evaluate jitter.
3. If jitter is acceptable (<1 frame), software sync may suffice; otherwise pursue hardware trigger.

When to ask for help
- If you want, provide photos or the exact stereo carrier/module model and I can draft a device-tree overlay tailored to it, and suggest kernel driver changes.
