`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/07/17 21:53:57
// Design Name: 
// Module Name: arbiterNC_FixedPriority
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description:  带有XOR-NC功能的arbiter。基于Fixed Priority策略。纯组合逻辑电路。
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
`include "design_params.vh "



////////////
module arbiterNC_FixedPriority(
    input wire [6 : 0] reqs,  // reqs: [0]-IP, [1]-W, [2]-E, [3]-S, [4]-N, [5]-D, [6]-U
    input wire [6 : 0] fifo_available, 
    
    input wire [`FLIT_AddressLenX -1 : 0] Local_AddrX,
    input wire [`FLIT_AddressLenY -1 : 0] Local_AddrY,
    input wire [`FLIT_AddressLenZ -1 : 0] Local_AddrZ, 
    
    input wire [`FLIT_BitWidth - 1 : 0] IPin_HeadFlit, Win_HeadFlit, Ein_HeadFlit, Sin_HeadFlit, Nin_HeadFlit, Din_HeadFlit, Uin_HeadFlit, 
    
    output reg [6 : 0] grants, // Which input req is granted: [0]-IP, [1]-W, [2]-E, [3]-S, [4]-N, [5]-D, [6]-U
    output reg [6 : 0] forwards, // The input packet is forwarded to: [0]-IP, [1]-W, [2]-E, [3]-S, [4]-N, [5]-D, [6]-U
    output reg NC_en
    );
    
    // Desti Address
    wire [`FLIT_AddressLenX -1 : 0] IPin_AddrX = IPin_HeadFlit[`HEADFLIT_AddressX_IDXBegin : `HEADFLIT_AddressX_IDXEnd]; 
    wire [`FLIT_AddressLenX -1 : 0] Win_AddrX = Win_HeadFlit[`HEADFLIT_AddressX_IDXBegin : `HEADFLIT_AddressX_IDXEnd]; 
    wire [`FLIT_AddressLenX -1 : 0] Ein_AddrX = Ein_HeadFlit[`HEADFLIT_AddressX_IDXBegin : `HEADFLIT_AddressX_IDXEnd]; 
    wire [`FLIT_AddressLenX -1 : 0] Sin_AddrX = Sin_HeadFlit[`HEADFLIT_AddressX_IDXBegin : `HEADFLIT_AddressX_IDXEnd];
    wire [`FLIT_AddressLenX -1 : 0] Nin_AddrX = Nin_HeadFlit[`HEADFLIT_AddressX_IDXBegin : `HEADFLIT_AddressX_IDXEnd];
    wire [`FLIT_AddressLenX -1 : 0] Din_AddrX = Din_HeadFlit[`HEADFLIT_AddressX_IDXBegin : `HEADFLIT_AddressX_IDXEnd];
    wire [`FLIT_AddressLenX -1 : 0] Uin_AddrX = Uin_HeadFlit[`HEADFLIT_AddressX_IDXBegin : `HEADFLIT_AddressX_IDXEnd];
    
    wire [`FLIT_AddressLenY -1 : 0] IPin_AddrY = IPin_HeadFlit[`HEADFLIT_AddressY_IDXBegin : `HEADFLIT_AddressY_IDXEnd]; 
    wire [`FLIT_AddressLenY -1 : 0] Win_AddrY = Win_HeadFlit[`HEADFLIT_AddressY_IDXBegin : `HEADFLIT_AddressY_IDXEnd]; 
    wire [`FLIT_AddressLenY -1 : 0] Ein_AddrY = Ein_HeadFlit[`HEADFLIT_AddressY_IDXBegin : `HEADFLIT_AddressY_IDXEnd]; 
    wire [`FLIT_AddressLenY -1 : 0] Sin_AddrY = Sin_HeadFlit[`HEADFLIT_AddressY_IDXBegin : `HEADFLIT_AddressY_IDXEnd];
    wire [`FLIT_AddressLenY -1 : 0] Nin_AddrY = Nin_HeadFlit[`HEADFLIT_AddressY_IDXBegin : `HEADFLIT_AddressY_IDXEnd];
    wire [`FLIT_AddressLenY -1 : 0] Din_AddrY = Din_HeadFlit[`HEADFLIT_AddressY_IDXBegin : `HEADFLIT_AddressY_IDXEnd];
    wire [`FLIT_AddressLenY -1 : 0] Uin_AddrY = Uin_HeadFlit[`HEADFLIT_AddressY_IDXBegin : `HEADFLIT_AddressY_IDXEnd];
    
    wire [`FLIT_AddressLenZ -1 : 0] IPin_AddrZ = IPin_HeadFlit[`HEADFLIT_AddressZ_IDXBegin : `HEADFLIT_AddressZ_IDXEnd]; 
    wire [`FLIT_AddressLenZ -1 : 0] Win_AddrZ = Win_HeadFlit[`HEADFLIT_AddressZ_IDXBegin : `HEADFLIT_AddressZ_IDXEnd]; 
    wire [`FLIT_AddressLenZ -1 : 0] Ein_AddrZ = Ein_HeadFlit[`HEADFLIT_AddressZ_IDXBegin : `HEADFLIT_AddressZ_IDXEnd]; 
    wire [`FLIT_AddressLenZ -1 : 0] Sin_AddrZ = Sin_HeadFlit[`HEADFLIT_AddressZ_IDXBegin : `HEADFLIT_AddressZ_IDXEnd];
    wire [`FLIT_AddressLenZ -1 : 0] Nin_AddrZ = Nin_HeadFlit[`HEADFLIT_AddressZ_IDXBegin : `HEADFLIT_AddressZ_IDXEnd];
    wire [`FLIT_AddressLenZ -1 : 0] Din_AddrZ = Din_HeadFlit[`HEADFLIT_AddressZ_IDXBegin : `HEADFLIT_AddressZ_IDXEnd];
    wire [`FLIT_AddressLenZ -1 : 0] Uin_AddrZ = Uin_HeadFlit[`HEADFLIT_AddressZ_IDXBegin : `HEADFLIT_AddressZ_IDXEnd];
    
    
    wire [`FLIT_AddressLenX -1 : 0] IPin_2ndAddrX = IPin_HeadFlit[`HEADFLIT_2ndAddressX_IDXBegin : `HEADFLIT_2ndAddressX_IDXEnd]; 
    wire [`FLIT_AddressLenX -1 : 0] Win_2ndAddrX = Win_HeadFlit[`HEADFLIT_2ndAddressX_IDXBegin : `HEADFLIT_2ndAddressX_IDXEnd]; 
    wire [`FLIT_AddressLenX -1 : 0] Ein_2ndAddrX = Ein_HeadFlit[`HEADFLIT_2ndAddressX_IDXBegin : `HEADFLIT_2ndAddressX_IDXEnd]; 
    wire [`FLIT_AddressLenX -1 : 0] Sin_2ndAddrX = Sin_HeadFlit[`HEADFLIT_2ndAddressX_IDXBegin : `HEADFLIT_2ndAddressX_IDXEnd];
    wire [`FLIT_AddressLenX -1 : 0] Nin_2ndAddrX = Nin_HeadFlit[`HEADFLIT_2ndAddressX_IDXBegin : `HEADFLIT_2ndAddressX_IDXEnd];
    wire [`FLIT_AddressLenX -1 : 0] Din_2ndAddrX = Din_HeadFlit[`HEADFLIT_2ndAddressX_IDXBegin : `HEADFLIT_2ndAddressX_IDXEnd];
    wire [`FLIT_AddressLenX -1 : 0] Uin_2ndAddrX = Uin_HeadFlit[`HEADFLIT_2ndAddressX_IDXBegin : `HEADFLIT_2ndAddressX_IDXEnd];
    
    wire [`FLIT_AddressLenY -1 : 0] IPin_2ndAddrY = IPin_HeadFlit[`HEADFLIT_2ndAddressY_IDXBegin : `HEADFLIT_2ndAddressY_IDXEnd]; 
    wire [`FLIT_AddressLenY -1 : 0] Win_2ndAddrY = Win_HeadFlit[`HEADFLIT_2ndAddressY_IDXBegin : `HEADFLIT_2ndAddressY_IDXEnd]; 
    wire [`FLIT_AddressLenY -1 : 0] Ein_2ndAddrY = Ein_HeadFlit[`HEADFLIT_2ndAddressY_IDXBegin : `HEADFLIT_2ndAddressY_IDXEnd]; 
    wire [`FLIT_AddressLenY -1 : 0] Sin_2ndAddrY = Sin_HeadFlit[`HEADFLIT_2ndAddressY_IDXBegin : `HEADFLIT_2ndAddressY_IDXEnd];
    wire [`FLIT_AddressLenY -1 : 0] Nin_2ndAddrY = Nin_HeadFlit[`HEADFLIT_2ndAddressY_IDXBegin : `HEADFLIT_2ndAddressY_IDXEnd];
    wire [`FLIT_AddressLenY -1 : 0] Din_2ndAddrY = Din_HeadFlit[`HEADFLIT_2ndAddressY_IDXBegin : `HEADFLIT_2ndAddressY_IDXEnd];
    wire [`FLIT_AddressLenY -1 : 0] Uin_2ndAddrY = Uin_HeadFlit[`HEADFLIT_2ndAddressY_IDXBegin : `HEADFLIT_2ndAddressY_IDXEnd];
    
    wire [`FLIT_AddressLenZ -1 : 0] IPin_2ndAddrZ = IPin_HeadFlit[`HEADFLIT_2ndAddressZ_IDXBegin : `HEADFLIT_2ndAddressZ_IDXEnd]; 
    wire [`FLIT_AddressLenZ -1 : 0] Win_2ndAddrZ = Win_HeadFlit[`HEADFLIT_2ndAddressZ_IDXBegin : `HEADFLIT_2ndAddressZ_IDXEnd]; 
    wire [`FLIT_AddressLenZ -1 : 0] Ein_2ndAddrZ = Ein_HeadFlit[`HEADFLIT_2ndAddressZ_IDXBegin : `HEADFLIT_2ndAddressZ_IDXEnd]; 
    wire [`FLIT_AddressLenZ -1 : 0] Sin_2ndAddrZ = Sin_HeadFlit[`HEADFLIT_2ndAddressZ_IDXBegin : `HEADFLIT_2ndAddressZ_IDXEnd];
    wire [`FLIT_AddressLenZ -1 : 0] Nin_2ndAddrZ = Nin_HeadFlit[`HEADFLIT_2ndAddressZ_IDXBegin : `HEADFLIT_2ndAddressZ_IDXEnd];
    wire [`FLIT_AddressLenZ -1 : 0] Din_2ndAddrZ = Din_HeadFlit[`HEADFLIT_2ndAddressZ_IDXBegin : `HEADFLIT_2ndAddressZ_IDXEnd];
    wire [`FLIT_AddressLenZ -1 : 0] Uin_2ndAddrZ = Uin_HeadFlit[`HEADFLIT_2ndAddressZ_IDXBegin : `HEADFLIT_2ndAddressZ_IDXEnd];
    
    wire [6 : 0] AddrCompare_IP, AddrCompare_W, AddrCompare_E, AddrCompare_S, AddrCompare_N, AddrCompare_D, AddrCompare_U;
    wire [6 : 0] AddrCompare2nd_W, AddrCompare2nd_E, AddrCompare2nd_S, AddrCompare2nd_N, AddrCompare2nd_D, AddrCompare2nd_U;
    
    // Compare Addresses
    // IP
    arbiterModule_AddrCompare AddrCmp_IP(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (IPin_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (IPin_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (IPin_AddrZ),
        .AddrDiff (AddrCompare_IP)  
        );
        
    // W & W2nd    
    arbiterModule_AddrCompare AddrCmp_W(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Win_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Win_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Win_AddrZ),
        .AddrDiff (AddrCompare_W)  
        );
        
    arbiterModule_AddrCompare AddrCmp2nd_W(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Win_2ndAddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Win_2ndAddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Win_2ndAddrZ),
        .AddrDiff (AddrCompare2nd_W)  
        );
    
    // E & E2nd    
    arbiterModule_AddrCompare AddrCmp_E(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Ein_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Ein_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Ein_AddrZ),
        .AddrDiff (AddrCompare_E)  
        );
        
    arbiterModule_AddrCompare AddrCmp2nd_E(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Ein_2ndAddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Ein_2ndAddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Ein_2ndAddrZ),
        .AddrDiff (AddrCompare2nd_E)  
        );
    
    // S & S2nd    
    arbiterModule_AddrCompare AddrCmp_S(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Sin_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Sin_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Sin_AddrZ),
        .AddrDiff (AddrCompare_S)  
        );
        
    arbiterModule_AddrCompare AddrCmp2nd_S(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Sin_2ndAddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Sin_2ndAddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Sin_2ndAddrZ),
        .AddrDiff (AddrCompare2nd_S)  
        );
   
   // N & N2nd     
    arbiterModule_AddrCompare AddrCmp_N(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Nin_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Nin_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Nin_AddrZ),
        .AddrDiff (AddrCompare_N)  
        );
        
    arbiterModule_AddrCompare AddrCmp2nd_N(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Nin_2ndAddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Nin_2ndAddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Nin_2ndAddrZ),
        .AddrDiff (AddrCompare2nd_N)  
        );
    
    // D & D2nd    
    arbiterModule_AddrCompare AddrCmp_D(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Din_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Din_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Din_AddrZ),
        .AddrDiff (AddrCompare_D) 
        );
        
    arbiterModule_AddrCompare AddrCmp2nd_D(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Din_2ndAddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Din_2ndAddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Din_2ndAddrZ),
        .AddrDiff (AddrCompare2nd_D) 
        );
    
    // U & U2nd    
    arbiterModule_AddrCompare AddrCmp_U(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Uin_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Uin_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Uin_AddrZ),
        .AddrDiff (AddrCompare_U)  
        );
        
    arbiterModule_AddrCompare AddrCmp2nd_U(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Uin_2ndAddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Uin_2ndAddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Uin_2ndAddrZ),
        .AddrDiff (AddrCompare2nd_U)  
        );


    // XYZ Alg
    wire [6 : 0] IP_XYZforward;  // 仅考虑XYZ规则，等待从IP端口输入的数据包的转发方向
    wire [6 : 0] W_XYZforward;
    wire [6 : 0] E_XYZforward;
    wire [6 : 0] S_XYZforward;
    wire [6 : 0] N_XYZforward;
    wire [6 : 0] D_XYZforward;
    wire [6 : 0] U_XYZforward;
    
    arbiterModule_AlgXYZ xyz_ip(
        .AddrDiff (AddrCompare_IP),
        .Forward_direction (IP_XYZforward)
    );
    
    arbiterModule_AlgXYZ xyz_w(
        .AddrDiff (AddrCompare_W),
        .Forward_direction (W_XYZforward)
    );
    
    arbiterModule_AlgXYZ xyz_e(
        .AddrDiff (AddrCompare_E),
        .Forward_direction (E_XYZforward)
    );
    
    arbiterModule_AlgXYZ xyz_s(
        .AddrDiff (AddrCompare_S),
        .Forward_direction (S_XYZforward)
    );
    
    arbiterModule_AlgXYZ xyz_n(
        .AddrDiff (AddrCompare_N),
        .Forward_direction (N_XYZforward)
    );
    
    arbiterModule_AlgXYZ xyz_d(
        .AddrDiff (AddrCompare_D),
        .Forward_direction (D_XYZforward)
    );
    
    arbiterModule_AlgXYZ xyz_u(
        .AddrDiff (AddrCompare_U),
        .Forward_direction (U_XYZforward)
    );

        
    // reqs state - Single - Uncoded
    wire [6 : 0] SU_reqs_state; // 0 - 无req或目标fifo已满;  1 - 有req且目标fifo可用
    wire [6 : 0] SU_IP_forward;  // 同时考虑XYZ规则与fifo状态，等待从IP端口输入的数据包的转发方向
    wire [6 : 0] SU_W_forward;
    wire [6 : 0] SU_E_forward;
    wire [6 : 0] SU_S_forward;
    wire [6 : 0] SU_N_forward;
    wire [6 : 0] SU_D_forward;
    wire [6 : 0] SU_U_forward; 
    
    assign SU_IP_forward = IP_XYZforward & fifo_available;
    assign SU_W_forward = W_XYZforward & fifo_available;
    assign SU_E_forward = E_XYZforward & fifo_available;
    assign SU_S_forward = S_XYZforward & fifo_available;
    assign SU_N_forward = N_XYZforward & fifo_available;
    assign SU_D_forward = D_XYZforward & fifo_available;
    assign SU_U_forward = U_XYZforward & fifo_available;
    
    assign SU_reqs_state[`IDX_IP] = ( |SU_IP_forward ) & reqs[`IDX_IP] & (~IPin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SU_reqs_state[`IDX_W] = ( |SU_W_forward ) & reqs[`IDX_W] & (~Win_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SU_reqs_state[`IDX_E] = ( |SU_E_forward ) & reqs[`IDX_E] & (~Ein_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SU_reqs_state[`IDX_S] = ( |SU_S_forward ) & reqs[`IDX_S] & (~Sin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SU_reqs_state[`IDX_N] = ( |SU_N_forward ) & reqs[`IDX_N] & (~Nin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SU_reqs_state[`IDX_D] = ( |SU_D_forward ) & reqs[`IDX_D] & (~Din_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SU_reqs_state[`IDX_U] = ( |SU_U_forward ) & reqs[`IDX_U] & (~Uin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    
    // reqs state - Single - Encoded
    wire [6 : 0] SE_reqs_state; // 0 - 无req或目标fifo已满;  1 - 有req且目标fifo可用
    wire [6 : 0] SE_W_forward;  // 针对已编码数据包的转发方向
    wire [6 : 0] SE_E_forward;
    wire [6 : 0] SE_S_forward;
    wire [6 : 0] SE_N_forward;
    wire [6 : 0] SE_D_forward;
    wire [6 : 0] SE_U_forward;     
    
    arbiterNCModule_FwEncoded_Win FwEncoded_W(
        .AddrCompare_P1 (AddrCompare_W), 
        .AddrCompare_P2 (AddrCompare2nd_W),
        .Forward_directions (SE_W_forward)
    );
    
    arbiterNCModule_FwEncoded_Ein FwEncoded_E(
        .AddrCompare_P1 (AddrCompare_E), 
        .AddrCompare_P2 (AddrCompare2nd_E),
        .Forward_directions (SE_E_forward)
    );
    
    arbiterNCModule_FwEncoded_Sin FwEncoded_S(
        .AddrCompare_P1 (AddrCompare_S), 
        .AddrCompare_P2 (AddrCompare2nd_S),
        .Forward_directions (SE_S_forward)
    );
    
    arbiterNCModule_FwEncoded_Nin FwEncoded_N(
        .AddrCompare_P1 (AddrCompare_N), 
        .AddrCompare_P2 (AddrCompare2nd_N),
        .Forward_directions (SE_N_forward)
    );
    
    arbiterNCModule_FwEncoded_Din FwEncoded_D(
        .AddrCompare_P1 (AddrCompare_D), 
        .AddrCompare_P2 (AddrCompare2nd_D),
        .Forward_directions (SE_D_forward)
    );
    
    arbiterNCModule_FwEncoded_Uin FwEncoded_U(
        .AddrCompare_P1 (AddrCompare_U), 
        .AddrCompare_P2 (AddrCompare2nd_U),
        .Forward_directions (SE_U_forward)
    );
    
    assign SE_reqs_state[`IDX_IP] = 1'b0;
    assign SE_reqs_state[`IDX_W] = reqs[`IDX_W] & ( ~( |( SE_W_forward & (~fifo_available) ) ) ) & (Win_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SE_reqs_state[`IDX_E] = reqs[`IDX_E] & ( ~( |( SE_E_forward & (~fifo_available) ) ) ) & (Ein_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SE_reqs_state[`IDX_S] = reqs[`IDX_S] & ( ~( |( SE_S_forward & (~fifo_available) ) ) ) & (Sin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SE_reqs_state[`IDX_N] = reqs[`IDX_N] & ( ~( |( SE_N_forward & (~fifo_available) ) ) ) & (Nin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SE_reqs_state[`IDX_D] = reqs[`IDX_D] & ( ~( |( SE_D_forward & (~fifo_available) ) ) ) & (Din_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign SE_reqs_state[`IDX_U] = reqs[`IDX_U] & ( ~( |( SE_U_forward & (~fifo_available) ) ) ) & (Uin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    
    // req state - NCEncoding
    wire NC_sat_WE, NC_sat_SN; 
    wire NCWE_req_state, NCSN_req_state;
    wire [6 : 0] NCWE_forward;  // 针对已编码数据包的转发方向
    wire [6 : 0] NCSN_forward;
      
    arbiterNCModule_EncodingRules_WE EncodingRules_WE(
        .W_AddrCompare (AddrCompare_W), 
        .E_AddrCompare (AddrCompare_E),
        .if_sat (NC_sat_WE),
        .Forward_directions (NCWE_forward)
    );
    
    arbiterNCModule_EncodingRules_SN EncodingRules_SN(
        .S_AddrCompare (AddrCompare_S), 
        .N_AddrCompare (AddrCompare_N),
        .if_sat (NC_sat_SN),
        .Forward_directions (NCSN_forward)
    );
    
    assign NCWE_req_state = reqs[`IDX_W] & reqs[`IDX_E] & ( ~( |( NCWE_forward & (~fifo_available) ) ) ) & (~Win_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]) & (~Ein_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    assign NCSN_req_state = reqs[`IDX_S] & reqs[`IDX_N] & ( ~( |( NCSN_forward & (~fifo_available) ) ) ) & (~Sin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]) & (~Nin_HeadFlit[`HEADFLIT_FlagIfEncoded_IDX]);
    
     // Arbiter
    always @(*) begin
        
        // Encoding
        if (NCWE_req_state) begin
            grants = 7'b00_00_11_0;
            forwards = NCWE_forward;
            NC_en = 1'b1;
        end
        
        else if (NCSN_req_state) begin
            grants = 7'b00_11_00_0;
            forwards = NCSN_forward;
            NC_en = 1'b1;
        end
        
        // IP
        else if (SU_reqs_state[`IDX_IP]) begin
            grants = 7'b00_00_00_1;
            forwards = SU_IP_forward;
            NC_en = 1'b0;
        end
        
        //W
        else if (SE_reqs_state[`IDX_W]) begin
            grants = 7'b00_00_01_0;
            forwards = SE_W_forward;
            NC_en = 1'b0;
        end
        
        else if (SU_reqs_state[`IDX_W]) begin
            grants = 7'b00_00_01_0;
            forwards = SU_W_forward;
            NC_en = 1'b0;
        end
        
        //E
        else if (SE_reqs_state[`IDX_E]) begin
            grants = 7'b00_00_10_0;
            forwards = SE_E_forward;
            NC_en = 1'b0;
        end
        
        else if (SU_reqs_state[`IDX_E]) begin
            grants = 7'b00_00_10_0;
            forwards = SU_E_forward;
            NC_en = 1'b0;
        end
        
        //S
        else if (SE_reqs_state[`IDX_S]) begin
            grants = 7'b00_01_00_0;
            forwards = SE_S_forward;
            NC_en = 1'b0;
        end
        
        else if (SU_reqs_state[`IDX_S]) begin
            grants = 7'b00_01_00_0;
            forwards = SU_S_forward;
            NC_en = 1'b0;
        end
        
        //N
        else if (SE_reqs_state[`IDX_N]) begin
            grants = 7'b00_10_00_0;
            forwards = SE_N_forward;
            NC_en = 1'b0;
        end
        
        else if (SU_reqs_state[`IDX_N]) begin
            grants = 7'b00_10_00_0;
            forwards = SU_N_forward;
            NC_en = 1'b0;
        end
        
        //D
        else if (SE_reqs_state[`IDX_D]) begin
            grants = 7'b01_00_00_0;
            forwards = SE_D_forward;
            NC_en = 1'b0;
        end
        
        else if (SU_reqs_state[`IDX_D]) begin
            grants = 7'b01_00_00_0;
            forwards = SU_D_forward;
            NC_en = 1'b0;
        end
        
        //U
        else if (SE_reqs_state[`IDX_U]) begin
            grants = 7'b10_00_00_0;
            forwards = SE_U_forward;
            NC_en = 1'b0;
        end
        
        else if (SU_reqs_state[`IDX_U]) begin
            grants = 7'b10_00_00_0;
            forwards = SU_U_forward;
            NC_en = 1'b0;
        end
        
        else begin
            grants = 7'b00_00_00_0;
            forwards = 7'b00_00_00_0;
            NC_en = 1'b0;
        end

        
    end
 
    
endmodule
////////////


