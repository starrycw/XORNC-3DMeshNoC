`ifndef __HEADER_design_params__
    `define __HEADER_design_params__
    
    // Flit
    `define FLIT_BitWidth 128  //Bit-width of each flit
    `define FLIT_AddressLenX 4  // Bit-width of the X-address in each head flit
    `define FLIT_AddressLenY 4
    `define FLIT_AddressLenZ 4
    
    `define HEADFLIT_FlagIfEncoded_IDX  (`FLIT_BitWidth - 3) // Idx of the flg bit that indicates whether the packet is encoded in the head flits.
    `define HEADFLIT_AddressX_IDXBegin (`FLIT_BitWidth - 4)
    `define HEADFLIT_AddressX_IDXEnd (`HEADFLIT_AddressX_IDXBegin - `FLIT_AddressLenX + 1)
    `define HEADFLIT_AddressY_IDXBegin (`HEADFLIT_AddressX_IDXEnd - 1)
    `define HEADFLIT_AddressY_IDXEnd (`HEADFLIT_AddressY_IDXBegin - `FLIT_AddressLenY + 1)
    `define HEADFLIT_AddressZ_IDXBegin (`HEADFLIT_AddressY_IDXEnd - 1)
    `define HEADFLIT_AddressZ_IDXEnd (`HEADFLIT_AddressZ_IDXBegin - `FLIT_AddressLenZ + 1)
    
    `define HEADFLIT_2ndAddressX_IDXBegin (`HEADFLIT_AddressZ_IDXEnd - 1)
    `define HEADFLIT_2ndAddressX_IDXEnd (`HEADFLIT_2ndAddressX_IDXBegin - `FLIT_AddressLenX + 1)
    `define HEADFLIT_2ndAddressY_IDXBegin (`HEADFLIT_2ndAddressX_IDXEnd - 1)
    `define HEADFLIT_2ndAddressY_IDXEnd (`HEADFLIT_2ndAddressY_IDXBegin - `FLIT_AddressLenY + 1)
    `define HEADFLIT_2ndAddressZ_IDXBegin (`HEADFLIT_2ndAddressY_IDXEnd - 1)
    `define HEADFLIT_2ndAddressZ_IDXEnd (`HEADFLIT_2ndAddressZ_IDXBegin - `FLIT_AddressLenZ + 1)
    
    // IDX
    `define IDX_IP 0
    `define IDX_W 1
    `define IDX_E 2
    `define IDX_S 3
    `define IDX_N 4
    `define IDX_D 5
    `define IDX_U 6
    
`endif