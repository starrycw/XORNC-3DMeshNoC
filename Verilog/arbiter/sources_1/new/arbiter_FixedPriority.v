`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/07/17 21:53:57
// Design Name: 
// Module Name: arbiter_FixedPriority
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description:  无NC的arbiter设计。基于Fixed Priority策略。纯组合逻辑电路。
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
module arbiter_FixedPriority(
    input wire [6 : 0] reqs,  // reqs: [0]-IP, [1]-W, [2]-E, [3]-S, [4]-N, [5]-D, [6]-U
    input wire [6 : 0] fifo_available, 
    
    input wire [`FLIT_AddressLenX -1 : 0] Local_AddrX,
    input wire [`FLIT_AddressLenY -1 : 0] Local_AddrY,
    input wire [`FLIT_AddressLenZ -1 : 0] Local_AddrZ, 
    
    input wire [`FLIT_BitWidth - 1 : 0] IPin_HeadFlit, Win_HeadFlit, Ein_HeadFlit, Sin_HeadFlit, Nin_HeadFlit, Din_HeadFlit, Uin_HeadFlit, 
    
    output reg [6 : 0] grants, // Which input req is granted: [0]-IP, [1]-W, [2]-E, [3]-S, [4]-N, [5]-D, [6]-U
    output reg [6 : 0] forwards // The input packet is forwarded to: [0]-IP, [1]-W, [2]-E, [3]-S, [4]-N, [5]-D, [6]-U
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
    
    wire [6 : 0] AddrCompare_IP, AddrCompare_W, AddrCompare_E, AddrCompare_S, AddrCompare_N, AddrCompare_D, AddrCompare_U;
    
    // Compare Addresses
    arbiterModule_AddrCompare AddrCmp_IP(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (IPin_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (IPin_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (IPin_AddrZ),
        .AddrDiff (AddrCompare_IP)  
        );
        
    arbiterModule_AddrCompare AddrCmp_W(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Win_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Win_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Win_AddrZ),
        .AddrDiff (AddrCompare_W)  
        );
        
    arbiterModule_AddrCompare AddrCmp_E(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Ein_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Ein_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Ein_AddrZ),
        .AddrDiff (AddrCompare_E)  
        );
        
    arbiterModule_AddrCompare AddrCmp_S(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Sin_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Sin_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Sin_AddrZ),
        .AddrDiff (AddrCompare_S)  
        );
        
    arbiterModule_AddrCompare AddrCmp_N(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Nin_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Nin_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Nin_AddrZ),
        .AddrDiff (AddrCompare_N)  
        );
        
    arbiterModule_AddrCompare AddrCmp_D(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Din_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Din_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Din_AddrZ),
        .AddrDiff (AddrCompare_D) 
        );
        
    arbiterModule_AddrCompare AddrCmp_U(
        .Local_AddrX (Local_AddrX), 
        .Desti_AddrX (Uin_AddrX),
        .Local_AddrY (Local_AddrY), 
        .Desti_AddrY (Uin_AddrY),
        .Local_AddrZ (Local_AddrZ), 
        .Desti_AddrZ (Uin_AddrZ),
        .AddrDiff (AddrCompare_U)  
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
    
        
    // reqs state
    wire [6 : 0] reqs_state; // 0 - 无req或目标fifo已满;  1 - 有req且目标fifo可用
    wire [6 : 0] IP_forward;  // 同时考虑XYZ规则与fifo状态，等待从IP端口输入的数据包的转发方向
    wire [6 : 0] W_forward;
    wire [6 : 0] E_forward;
    wire [6 : 0] S_forward;
    wire [6 : 0] N_forward;
    wire [6 : 0] D_forward;
    wire [6 : 0] U_forward; 
    
    assign IP_forward = IP_XYZforward & fifo_available;
    assign W_forward = W_XYZforward & fifo_available;
    assign E_forward = E_XYZforward & fifo_available;
    assign S_forward = S_XYZforward & fifo_available;
    assign N_forward = N_XYZforward & fifo_available;
    assign D_forward = D_XYZforward & fifo_available;
    assign U_forward = U_XYZforward & fifo_available;
    
    assign reqs_state[`IDX_IP] = ( |IP_forward ) & reqs[`IDX_IP];
    assign reqs_state[`IDX_W] = ( |W_forward ) & reqs[`IDX_W];
    assign reqs_state[`IDX_E] = ( |E_forward ) & reqs[`IDX_E];
    assign reqs_state[`IDX_S] = ( |S_forward ) & reqs[`IDX_S];
    assign reqs_state[`IDX_N] = ( |N_forward ) & reqs[`IDX_N];
    assign reqs_state[`IDX_D] = ( |D_forward ) & reqs[`IDX_D];
    assign reqs_state[`IDX_U] = ( |U_forward ) & reqs[`IDX_U];
        
     // Arbiter
    always @(*) begin
        if (reqs_state[`IDX_IP]) begin
            grants = 7'b00_00_00_1;
            forwards = IP_forward;
        end
        
        else if (reqs_state[`IDX_W]) begin
            grants = 7'b00_00_01_0;
            forwards = W_forward;
        end
        
        else if (reqs_state[`IDX_E]) begin
            grants = 7'b00_00_10_0;
            forwards = E_forward;
        end
        
        else if (reqs_state[`IDX_S]) begin
            grants = 7'b00_01_00_0;
            forwards = S_forward;
        end
        
        else if (reqs_state[`IDX_N]) begin
            grants = 7'b00_10_00_0;
            forwards = N_forward;
        end
        
        else if (reqs_state[`IDX_D]) begin
            grants = 7'b01_00_00_0;
            forwards = D_forward;
        end
        
        else if (reqs_state[`IDX_U]) begin
            grants = 7'b10_00_00_0;
            forwards = U_forward;
        end
        
        else begin
            grants = 7'b00_00_00_0;
            forwards = 7'b00_00_00_0;
        end
    end
    
//////////////////////////////////////////////////////////////////////////////////DELETE    
//
//    // reqs state 
//    arbiterModule_ReqAnalyze reqanalyze_IP(
//        .req (req[`IDX_IP]),
//        .fifo_available (fifo_available[`IDX_IP]),
//        .Local_AddrX (Local_AddrX), 
//        .Desti_AddrX (IPin_AddrX),
//        .Local_AddrY (Local_AddrY), 
//        .Desti_AddrY (IPin_AddrY),
//        .Local_AddrZ (Local_AddrZ), 
//        .Desti_AddrZ (IPin_AddrZ),
//        .req_state (reqs_state[`IDX_IP]),
//        .forward_flags (IP_forward)
//    );
//    
//    arbiterModule_ReqAnalyze reqanalyze_W(
//        .req (req[`IDX_W]),
//        .fifo_available (fifo_available[`IDX_W]),
//        .Local_AddrX (Local_AddrX), 
//        .Desti_AddrX (Win_AddrX),
//        .Local_AddrY (Local_AddrY), 
//        .Desti_AddrY (Win_AddrY),
//        .Local_AddrZ (Local_AddrZ), 
//        .Desti_AddrZ (Win_AddrZ),
//        .req_state (reqs_state[`IDX_W]),
//        .forward_flags (W_forward)
//    );
//    
//    arbiterModule_ReqAnalyze reqanalyze_E(
//        .req (req[`IDX_E]),
//        .fifo_available (fifo_available[`IDX_E]),
//        .Local_AddrX (Local_AddrX), 
//        .Desti_AddrX (Ein_AddrX),
//        .Local_AddrY (Local_AddrY), 
//        .Desti_AddrY (Ein_AddrY),
//        .Local_AddrZ (Local_AddrZ), 
//        .Desti_AddrZ (Ein_AddrZ),
//        .req_state (reqs_state[`IDX_E]),
//        .forward_flags (E_forward)
//    );
//    
//    arbiterModule_ReqAnalyze reqanalyze_S(
//        .req (req[`IDX_S]),
//        .fifo_available (fifo_available[`IDX_S]),
//        .Local_AddrX (Local_AddrX), 
//        .Desti_AddrX (Sin_AddrX),
//        .Local_AddrY (Local_AddrY), 
//        .Desti_AddrY (Sin_AddrY),
//        .Local_AddrZ (Local_AddrZ), 
//        .Desti_AddrZ (Sin_AddrZ),
//        .req_state (reqs_state[`IDX_S]),
//        .forward_flags (S_forward)
//    );
//    
//    arbiterModule_ReqAnalyze reqanalyze_N(
//        .req (req[`IDX_N]),
//        .fifo_available (fifo_available[`IDX_N]),
//        .Local_AddrX (Local_AddrX), 
//        .Desti_AddrX (Nin_AddrX),
//        .Local_AddrY (Local_AddrY), 
//        .Desti_AddrY (Nin_AddrY),
//        .Local_AddrZ (Local_AddrZ), 
//        .Desti_AddrZ (Nin_AddrZ),
//        .req_state (reqs_state[`IDX_N]),
//        .forward_flags (N_forward)
//    );
//    
//    arbiterModule_ReqAnalyze reqanalyze_D(
//        .req (req[`IDX_D]),
//        .fifo_available (fifo_available[`IDX_D]),
//        .Local_AddrX (Local_AddrX), 
//        .Desti_AddrX (Din_AddrX),
//        .Local_AddrY (Local_AddrY), 
//        .Desti_AddrY (Din_AddrY),
//        .Local_AddrZ (Local_AddrZ), 
//        .Desti_AddrZ (Din_AddrZ),
//        .req_state (reqs_state[`IDX_D]),
//        .forward_flags (D_forward)
//    );
//    
//    arbiterModule_ReqAnalyze reqanalyze_U(
//        .req (req[`IDX_U]),
//        .fifo_available (fifo_available[`IDX_U]),
//        .Local_AddrX (Local_AddrX), 
//        .Desti_AddrX (Uin_AddrX),
//        .Local_AddrY (Local_AddrY), 
//        .Desti_AddrY (Uin_AddrY),
//        .Local_AddrZ (Local_AddrZ), 
//        .Desti_AddrZ (Uin_AddrZ),
//        .req_state (reqs_state[`IDX_U]),
//        .forward_flags (U_forward)
//    );
//////////////////////////////////////////////////////////////////////////////////DELETE    
    
   
    
    
endmodule
////////////
