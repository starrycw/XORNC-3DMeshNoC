import copy
import time
from random import choice
import NoC_Designs.NoCs_top as imported_NoCs_top
import SimuConfigurationClass as imported_SimuConfigurationClass

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
### Number of cases
simuParam_case_max = 10000
### Number of multicast tasks in each case
simuParam_task_max = 1
### NoC models. In each case, the tasks injected into these NoC models have the SAME src and des addresses and DIFFERENT number of payload flits.
simuParam_nModels_VaPayloads = 12 # Number of models
simuParam_nPayloadFlit_min = 3 # The min number of payload flits in each data package. This min number is for the first model.
simuParam_nPayloadFlit_increase = 1
### task constraints
simuParam_task_nSrc = 2
simuParam_task_nDes = 4
simuParam_task_srcAddrZ_tuple = (0,)
simuParam_task_desAddrZ_tuple = (1, 2, 3)
simuParam_task_srcAddrX_tuple = (0, NoCParam_nX - 1)
simuParam_task_desAddrX_tuple = tuple(range(0, NoCParam_nX))
# simuParam_task_srcAddrY_tuple = None
simuParam_task_desAddrY_tuple = tuple(range(0, NoCParam_nY))

### Stastical
simustat_cntHopsList = []
simustat_maxHopsList = []
simustat_minHopsList = []
simustat_cntHopsList_temp = []
for idx_aaa in range(0, simuParam_nModels_VaPayloads):
    simustat_cntHopsList.append([0, 0]) # [nSteps_FP, nSteps_NCFP]
    simustat_maxHopsList.append([0, 0])
    simustat_minHopsList.append([100000, 100000])
    simustat_cntHopsList_temp.append([0, 0])


# File
logName_str = "NoC{}_{}_{}_nSrc{}_nDes{}_Time{}".format(copy.deepcopy(NoCParam_nX),
                                                        copy.deepcopy(NoCParam_nY),
                                                        copy.deepcopy(NoCParam_nZ),
                                                        copy.deepcopy(simuParam_task_nSrc),
                                                        copy.deepcopy(simuParam_task_nDes),
                                                        time.time())


for simu_case_i in range(0, simuParam_case_max):
    # Generate Src
    simuParam_task_srcAddrY_tuple = (choice(tuple(range(0, NoCParam_nY))),)
    genSrc_list = []
    while len(genSrc_list) < simuParam_task_nSrc:
        genSrcAddr_Z = choice(simuParam_task_srcAddrZ_tuple)
        genSrcAddr_X = choice(simuParam_task_srcAddrX_tuple)
        genSrcAddr_Y = choice(simuParam_task_srcAddrY_tuple)
        if_sat = True
        for existSrc_i in copy.deepcopy(genSrc_list):
            if (genSrcAddr_X == existSrc_i[0]) and (genSrcAddr_Y == existSrc_i[1]) and (genSrcAddr_Z == existSrc_i[2]):
                if_sat = False
        genSrc_current = (copy.deepcopy(genSrcAddr_X), copy.deepcopy(genSrcAddr_Y), copy.deepcopy(genSrcAddr_Z))
        if if_sat is True:
            genSrc_list.append(copy.deepcopy(genSrc_current))

    # Generate Des
    genDes_list = []
    while len(genDes_list) < simuParam_task_nDes:
        genDesAddr_Z = choice(simuParam_task_desAddrZ_tuple)
        genDesAddr_X = choice(simuParam_task_desAddrX_tuple)
        genDesAddr_Y = choice(simuParam_task_desAddrY_tuple)
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
        desListOfEachSrc.append(tuple(copy.deepcopy(genDes_list)))
        # currentDesList.insert(0, currentDesList.pop())


    NoC_ModelsList = []
    for idx_nmodels_i in range(0, simuParam_nModels_VaPayloads):
        NoC_FP_gen = imported_NoCs_top.NoCTop_FP(nX=NoCParam_nX, nY=NoCParam_nY, nZ=NoCParam_nZ,
                                                 SimuConfig_instance=ConfigInst)
        NoC_NCFP_gen = imported_NoCs_top.NoCTop_NCFP(nX=NoCParam_nX, nY=NoCParam_nY, nZ=NoCParam_nZ,
                                                     SimuConfig_instance=ConfigInst)
        NoC_ModelsList.append([copy.deepcopy(NoC_FP_gen), copy.deepcopy(NoC_NCFP_gen)])

    simustat_cntHopsList_temp = []
    for idx_aaabbb in range(0, simuParam_nModels_VaPayloads):
        simustat_cntHopsList_temp.append([0, 0])

    for simu_task_i in range(0, simuParam_task_max):
        # Inject packets
        for idx_src_i in range(0, simuParam_task_nSrc):
            for idx_des_of_src_i in range(0, simuParam_task_nDes):
                flitGen_srcAddr = copy.deepcopy(genSrc_list[idx_src_i])
                flitGen_desAddr = copy.deepcopy(desListOfEachSrc[idx_src_i][idx_des_of_src_i])
                nPayloadFlit_current = simuParam_nPayloadFlit_min
                for idx_nmodels_injii in range(0, simuParam_nModels_VaPayloads):
                    # Head
                    NoC_ModelsList[idx_nmodels_injii][0].Update_injectFlit(routerAddr=flitGen_srcAddr,
                                                                           injectedFlit_tuple=ConfigInst.flitGenerate_Head(sourceAddr_tuple=flitGen_srcAddr,
                                                                                                                           destiAddr_tuple=flitGen_desAddr)
                                                                           )
                    NoC_ModelsList[idx_nmodels_injii][1].Update_injectFlit(routerAddr=flitGen_srcAddr,
                                                                           injectedFlit_tuple=ConfigInst.flitGenerate_Head(
                                                                               sourceAddr_tuple=flitGen_srcAddr,
                                                                               destiAddr_tuple=flitGen_desAddr)
                                                                           )

                    # Payloads
                    for flitGen_idx_i in range(0, nPayloadFlit_current):
                        NoC_ModelsList[idx_nmodels_injii][0].Update_injectFlit(routerAddr=flitGen_srcAddr,
                                                                               injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())
                        NoC_ModelsList[idx_nmodels_injii][1].Update_injectFlit(routerAddr=flitGen_srcAddr,
                                                                               injectedFlit_tuple=ConfigInst.flitGenerate_randomPayload())

                    nPayloadFlit_current = nPayloadFlit_current + simuParam_nPayloadFlit_increase

                    # Tail
                    NoC_ModelsList[idx_nmodels_injii][0].Update_injectFlit(routerAddr=flitGen_srcAddr,
                                                                           injectedFlit_tuple=ConfigInst.flitGenerate_Tail())
                    NoC_ModelsList[idx_nmodels_injii][1].Update_injectFlit(routerAddr=flitGen_srcAddr,
                                                                           injectedFlit_tuple=ConfigInst.flitGenerate_Tail())





        # Multicast
        for idx_mucpre_i in range(0, simuParam_nModels_VaPayloads):
            for temp_secAddr_i in copy.deepcopy(genSrc_list):
                while NoC_ModelsList[idx_mucpre_i][0].getFIFOState_ifEmpty_byLocalRouter_byPortName(
                        localRouterAddr=copy.deepcopy(temp_secAddr_i), portName="IP_In") is False:
                    NoC_ModelsList[idx_mucpre_i][0].UpdateOneRouter_oneCycle(idx_xi=temp_secAddr_i[0],
                                                                             idx_yi=temp_secAddr_i[1],
                                                                             idx_zi=temp_secAddr_i[2])

                while NoC_ModelsList[idx_mucpre_i][1].getFIFOState_ifEmpty_byLocalRouter_byPortName(
                        localRouterAddr=copy.deepcopy(temp_secAddr_i), portName="IP_In") is False:
                    NoC_ModelsList[idx_mucpre_i][1].UpdateOneRouter_oneCycle(idx_xi=temp_secAddr_i[0],
                                                                             idx_yi=temp_secAddr_i[1],
                                                                             idx_zi=temp_secAddr_i[2])



        # Run
        for idx_runmodels_mii in range(0, simuParam_nModels_VaPayloads):
            while NoC_ModelsList[idx_runmodels_mii][0].getNoCState_ifAllTaskCompleted()[0] is False:
                NoC_ModelsList[idx_runmodels_mii][0].Update_oneCycle()
                simustat_cntHopsList_temp[idx_runmodels_mii][0] = simustat_cntHopsList_temp[idx_runmodels_mii][0] + 1

            while NoC_ModelsList[idx_runmodels_mii][1].getNoCState_ifAllTaskCompleted()[0] is False:
                NoC_ModelsList[idx_runmodels_mii][1].Update_oneCycle()
                simustat_cntHopsList_temp[idx_runmodels_mii][1] = simustat_cntHopsList_temp[idx_runmodels_mii][1] + 1



    for idx_simucntmodels_iii in range(0, simuParam_nModels_VaPayloads):
        simustat_cntHopsList[idx_simucntmodels_iii][0] = simustat_cntHopsList[idx_simucntmodels_iii][0] + simustat_cntHopsList_temp[idx_simucntmodels_iii][0]
        simustat_cntHopsList[idx_simucntmodels_iii][1] = simustat_cntHopsList[idx_simucntmodels_iii][1] + simustat_cntHopsList_temp[idx_simucntmodels_iii][1]

        if simustat_maxHopsList[idx_simucntmodels_iii][0] < simustat_cntHopsList_temp[idx_simucntmodels_iii][0]:
            simustat_maxHopsList[idx_simucntmodels_iii][0] = simustat_cntHopsList_temp[idx_simucntmodels_iii][0]

        if simustat_maxHopsList[idx_simucntmodels_iii][1] < simustat_cntHopsList_temp[idx_simucntmodels_iii][1]:
            simustat_maxHopsList[idx_simucntmodels_iii][1] = simustat_cntHopsList_temp[idx_simucntmodels_iii][1]

        if simustat_minHopsList[idx_simucntmodels_iii][0] > simustat_cntHopsList_temp[idx_simucntmodels_iii][0]:
            simustat_minHopsList[idx_simucntmodels_iii][0] = simustat_cntHopsList_temp[idx_simucntmodels_iii][0]

        if simustat_minHopsList[idx_simucntmodels_iii][1] > simustat_cntHopsList_temp[idx_simucntmodels_iii][1]:
            simustat_minHopsList[idx_simucntmodels_iii][1] = simustat_cntHopsList_temp[idx_simucntmodels_iii][1]

    print("Case ", simu_case_i, " Finished! SRC:", genSrc_list, "; DES:", genDes_list)
    print(">> stat-Hops-current: ", simustat_cntHopsList_temp)
    print(">> stat-Hops-all: ", simustat_cntHopsList)
    print(">> stat-Hops-max: ", simustat_maxHopsList)
    print(">> stat-Hops-min: ", simustat_minHopsList)
    with open(logPath_str + "/simu_logs/" + logName_str + ".txt", "a") as log_f:
        log_f.write("\n Case-{}, stat-Hops-current-{}, stat-Hops-all-{}, stat-Hops-max-{}, stat-Hops-min-{}".format(simu_case_i, simustat_cntHopsList_temp, simustat_cntHopsList, simustat_maxHopsList, simustat_minHopsList))

print(" --------- ALL DONE! --------- ")
print(simustat_cntHopsList)
print(simustat_maxHopsList)
print(simustat_minHopsList)