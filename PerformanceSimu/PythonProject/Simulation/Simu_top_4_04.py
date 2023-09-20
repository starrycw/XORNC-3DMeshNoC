# Simu_top
import copy
import time
from random import choice
import NoC_Designs.NoCs_top as imported_NoCs_top
import SimuConfigurationClass as imported_SimuConfigurationClass

# ########################################################################################################################
# ConfigInst = imported_SimuConfigurationClass.SimuConfigs(param_flitBitWidth=128,
#                                                          param_addrBitWidth_tuple =(4, 4, 4),
#                                                          param_FIFOFlitDepth=20,
#                                                          param_IP_FlitSent_nMax=10000,
#                                                          param_IP_FlitReceive_nMax=10000)
#
# # NoCModel = imported_NoCs_top.NoCTop_FP(nX=4, nY=4, nZ=4, SimuConfig_instance=ConfigInst) # FP Model
# NoCModel = imported_NoCs_top.NoCTop_NCFP(nX=4, nY=4, nZ=4, SimuConfig_instance=ConfigInst) # NCFP Model
#
# task1_src = (0, 0, 0)
# task1_dest = (1, 3, 3)
# task2_src = (2, 0, 0)
# task2_dest = (0, 3, 3)
#
# NoCModel.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=ConfigInst.flitGenerate_Head(sourceAddr_tuple=task1_src, destiAddr_tuple=task1_dest))
# NoCModel.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())
# NoCModel.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())
# NoCModel.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())
# NoCModel.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=ConfigInst.flitGenerate_Tail())
#
# NoCModel.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=ConfigInst.flitGenerate_Head(sourceAddr_tuple=task2_src, destiAddr_tuple=task2_dest))
# NoCModel.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())
# NoCModel.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())
# NoCModel.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())
# NoCModel.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=ConfigInst.flitGenerate_Tail())
#
# for i in range(20):
#     print("Step ", i)
#     NoCModel.Update_oneCycle()
#     print("TASK1-DES - ", NoCModel.readOut_IPReceivedFlits(routerAddr=task1_dest))
#     print("TASK2-DES - ", NoCModel.readOut_IPReceivedFlits(routerAddr=task2_dest))
#     print("Node (1,0,0) - ", NoCModel.readOnly_currentRouterStates(routerAddr=(1, 0, 0)))
#     print("##############################################################################")
# ########################################################################################################################

########################################################################################################################
# main
########################################################################################################################

# Configuration
NoCParam_nX = 4
NoCParam_nY = 4
NoCParam_nZ = 4
logPath_str = "/home/cwei/eda/Workspace/PyCharm_Workspace/XOR-NC"

ConfigInst = imported_SimuConfigurationClass.SimuConfigs(param_flitBitWidth=128,
                                                         param_addrBitWidth_tuple=(4, 4, 4),
                                                         param_FIFOFlitDepth=100000,
                                                         param_IP_FlitSent_nMax=100000,
                                                         param_IP_FlitReceive_nMax=100000)

# Simulation Config
simuParam_case_max = 10000
simuParam_task_max = 1
simuParam_nPayloadFlit = 3
simuParam_task_nSrc = 2
simuParam_task_nDes = 4
simuParam_task_srcAddrZ_tuple = (0,)
simuParam_task_desAddrZ_tuple = (1, 2, 3)
cnt_stepsSumAllCase_FP = 0
cnt_stepsSumAllCase_NCFP = 0
maxHop_FP = 0
minHop_FP = 100000
maxHop_NCFP = 0
minHop_NCFP = 100000

# File
logName_str = "NoC{}_{}_{}_nSrc{}_nDes{}_Time{}".format(copy.deepcopy(NoCParam_nX),
                                                        copy.deepcopy(NoCParam_nY),
                                                        copy.deepcopy(NoCParam_nZ),
                                                        copy.deepcopy(simuParam_task_nSrc),
                                                        copy.deepcopy(simuParam_task_nDes),
                                                        time.time())

for simu_case_i in range(0, simuParam_case_max):
    # Generate Src and Des
    #AddrX_tuple_src = tuple(range(0, NoCParam_nX))
    AddrX_tuple_src = (0, NoCParam_nX - 1)
    AddrY_tuple_src = (choice(tuple(range(0, NoCParam_nY))),)
    # AddrY_tuple_src = tuple(range(0, NoCParam_nY))
    AddrX_tuple_des = tuple(range(0, NoCParam_nX))
    AddrY_tuple_des = tuple(range(0, NoCParam_nY))
    genSrc_list = []
    genDes_list = []
    while len(genSrc_list) < simuParam_task_nSrc:
        genSrcAddr_Z = choice(simuParam_task_srcAddrZ_tuple)
        genSrcAddr_X = choice(AddrX_tuple_src)
        genSrcAddr_Y = choice(AddrY_tuple_src)
        if_sat = True
        for existSrc_i in copy.deepcopy(genSrc_list):
            if (genSrcAddr_X == existSrc_i[0]) and (genSrcAddr_Y == existSrc_i[1]) and (genSrcAddr_Z == existSrc_i[2]):
                if_sat = False
        genSrc_current = (copy.deepcopy(genSrcAddr_X), copy.deepcopy(genSrcAddr_Y), copy.deepcopy(genSrcAddr_Z))
        if if_sat is True:
            genSrc_list.append(copy.deepcopy(genSrc_current))

    while len(genDes_list) < simuParam_task_nDes:
        genDesAddr_Z = choice(simuParam_task_desAddrZ_tuple)
        genDesAddr_X = choice(AddrX_tuple_des)
        genDesAddr_Y = choice(AddrY_tuple_des)
        if_sat = True
        for existDes_i in copy.deepcopy(genDes_list):
            if (genDesAddr_X == existDes_i[0]) and (genDesAddr_Y == existDes_i[1]) and (genDesAddr_Z == existDes_i[2]):
                if_sat = False
        genDes_current = (copy.deepcopy(genDesAddr_X), copy.deepcopy(genDesAddr_Y), copy.deepcopy(genDesAddr_Z))
        if if_sat is True:
            genDes_list.append(copy.deepcopy(genDes_current))

    # Start Tasks
    desListOfEachSrc = []
    for idx_k in range(0, simuParam_task_nSrc):
        currentDesList = list(copy.deepcopy(genDes_list))
        desListOfEachSrc.append(tuple(copy.deepcopy(currentDesList)))
        currentDesList.insert(0, currentDesList.pop())


    cnt_stepsSum_FP = 0
    cnt_stepsSum_NCFP = 0
    NoC_FP = imported_NoCs_top.NoCTop_FP(nX=NoCParam_nX, nY=NoCParam_nY, nZ=NoCParam_nZ,
                                         SimuConfig_instance=ConfigInst)
    NoC_NCFP = imported_NoCs_top.NoCTop_NCFP(nX=NoCParam_nX, nY=NoCParam_nY, nZ=NoCParam_nZ,
                                             SimuConfig_instance=ConfigInst)

    for simu_task_i in range(0, simuParam_task_max):
        # Inject packets
        for idx_src_i in range(0, simuParam_task_nSrc):
            for idx_des_of_src_i in range(0, simuParam_task_nDes):
                flitGen_srcAddr = copy.deepcopy(genSrc_list[idx_src_i])
                flitGen_desAddr = copy.deepcopy(desListOfEachSrc[idx_src_i][idx_des_of_src_i])
                NoC_FP.Update_injectFlit(routerAddr=flitGen_srcAddr,
                                         injectedFlit_tuple=ConfigInst.flitGenerate_Head(sourceAddr_tuple=flitGen_srcAddr,
                                                                                         destiAddr_tuple=flitGen_desAddr)
                                         )
                NoC_NCFP.Update_injectFlit(routerAddr=flitGen_srcAddr,
                                           injectedFlit_tuple=ConfigInst.flitGenerate_Head(sourceAddr_tuple=flitGen_srcAddr,
                                                                                           destiAddr_tuple=flitGen_desAddr)
                                           )

                for flitGen_idx_i in range(0, simuParam_nPayloadFlit):
                    NoC_FP.Update_injectFlit(routerAddr=flitGen_srcAddr,
                                             injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())
                    NoC_NCFP.Update_injectFlit(routerAddr=flitGen_srcAddr,
                                               injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())

                NoC_FP.Update_injectFlit(routerAddr=flitGen_srcAddr,
                                         injectedFlit_tuple=ConfigInst.flitGenerate_Tail())
                NoC_NCFP.Update_injectFlit(routerAddr=flitGen_srcAddr,
                                           injectedFlit_tuple=ConfigInst.flitGenerate_Tail())


        # Multicast
        for temp_secAddr_i in copy.deepcopy(genSrc_list):
            while NoC_FP.getFIFOState_ifEmpty_byLocalRouter_byPortName(localRouterAddr=copy.deepcopy(temp_secAddr_i), portName="IP_In") is False:
                NoC_FP.UpdateOneRouter_oneCycle(idx_xi=temp_secAddr_i[0], idx_yi=temp_secAddr_i[1], idx_zi=temp_secAddr_i[2])
            while NoC_NCFP.getFIFOState_ifEmpty_byLocalRouter_byPortName(localRouterAddr=copy.deepcopy(temp_secAddr_i), portName="IP_In") is False:
                NoC_NCFP.UpdateOneRouter_oneCycle(idx_xi=temp_secAddr_i[0], idx_yi=temp_secAddr_i[1], idx_zi=temp_secAddr_i[2])

        # Run
        stepCnt_FP = 0
        while NoC_FP.getNoCState_ifAllTaskCompleted()[0] is False:
            # print(NoC_FP.getNoCState_ifAllTaskCompleted()[1])
            NoC_FP.Update_oneCycle()
            stepCnt_FP = stepCnt_FP + 1

        stepCnt_NCFP = 0
        while NoC_NCFP.getNoCState_ifAllTaskCompleted()[0] is False:
            NoC_NCFP.Update_oneCycle()
            stepCnt_NCFP = stepCnt_NCFP + 1

        cnt_stepsSum_FP = cnt_stepsSum_FP + stepCnt_FP
        cnt_stepsSum_NCFP = cnt_stepsSum_NCFP + stepCnt_NCFP
        # print("Case ", simu_case_i, ", Task ", simu_task_i, " - stepCnt_FP=", stepCnt_FP, "; stepCnt_NCFP=", stepCnt_NCFP)

    cnt_stepsSumAllCase_FP = cnt_stepsSumAllCase_FP + cnt_stepsSum_FP
    cnt_stepsSumAllCase_NCFP = cnt_stepsSumAllCase_NCFP + cnt_stepsSum_NCFP
    print("Case ", simu_case_i, " Finished! SRC:", genSrc_list, "; DES:", genDes_list, "; MIN-MAX:", minHop_FP, maxHop_FP, minHop_NCFP, maxHop_NCFP)
    print("FP: (+", cnt_stepsSum_FP, ") ", cnt_stepsSumAllCase_FP, "; NCFP: (+", cnt_stepsSum_NCFP, ") ", cnt_stepsSumAllCase_NCFP)
    with open(logPath_str + "/simu_logs/" + logName_str + ".txt", "a") as log_f:
        log_f.write("\n Case-{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(simu_case_i, cnt_stepsSum_FP, cnt_stepsSumAllCase_FP, cnt_stepsSum_NCFP, cnt_stepsSumAllCase_NCFP, minHop_FP, maxHop_FP, minHop_NCFP, maxHop_NCFP, genSrc_list, genDes_list))
    if maxHop_FP < cnt_stepsSum_FP:
        maxHop_FP = cnt_stepsSum_FP
    if minHop_FP > cnt_stepsSum_FP:
        minHop_FP = cnt_stepsSum_FP
    if maxHop_NCFP < cnt_stepsSum_NCFP:
        maxHop_NCFP = cnt_stepsSum_NCFP
    if minHop_NCFP > cnt_stepsSum_NCFP:
        minHop_NCFP = cnt_stepsSum_NCFP
print("### ALL DONE! -- ", maxHop_FP, minHop_FP, maxHop_NCFP, minHop_NCFP)
















########################################################################################################################

