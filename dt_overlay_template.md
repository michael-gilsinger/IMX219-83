Device-Tree Overlay Template for dual IMX219-83 on Jetson Orin Nano Super

This is a generic template — adapt the node names, clocks, and endpoints to match your carrier board and CSI connectors.

Notes:
- Jetson device-tree bindings change between L4T versions — test carefully.
- For Orin/Orin Nano you will usually modify a board-specific dtsi or use a Jetson-compatible overlay.

Example fragment (informational only):

/ {
    camera@0 {
        compatible = "sony,imx219";
        reg = <0>;
        status = "okay";
        /* clocks, reset-gpios, i2c info here */
        port@0 {
            reg = <0>;
            imx219_ep: endpoint {
                remote-endpoint = <&vi2c 0>;
                bus-width = <2>;
                /* ... */
            };
        };
    };

    camera@1 {
        compatible = "sony,imx219";
        reg = <1>;
        status = "okay";
        port@0 {
            reg = <0>;
            imx219_ep2: endpoint {
                remote-endpoint = <&vi2c 1>;
                bus-width = <2>;
            };
        };
    };
};

Important: this is only a starting point. For JetPack 6.x inspect the `/boot/dtb/` for your Orin Nano device tree, and examine existing camera node examples in the L4T kernel sources. If you're using an Arducam or third-party stereo module, follow their provided overlay and adapt sensor indices.
