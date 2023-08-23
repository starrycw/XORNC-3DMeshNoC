# Simu_top

import NoC_Designs.NoCs_top as imported_NoCs_top
import SimuConfigurationClass as imported_ActiveConfiguration

########################################################################################################################
# Configuration
SimuConfigInstance = imported_ActiveConfiguration.SimuConfigs(param_flitBitWidth=128,
                                                         param_addrBitWidth_tuple =(4, 4, 4),
                                                         param_FIFOFlitDepth=20,
                                                         param_IP_FlitSent_nMax=10000,
                                                         param_IP_FlitReceive_nMax=10000)

NoCModel_FP_Instance = imported_NoCs_top.NoCTop_FP(nX=3, nY=3, nZ=3, SimuConfig_instance=SimuConfigInstance)


task1_src = (0, 0, 0)
task1_dest = (1, 2, 2)
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_Head(sourceAddr_tuple=task1_src, destiAddr_tuple=task1_dest))

NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())

NoCModel_FP_Instance.Update_injectFlit(routerAddr=task1_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_Tail())


task2_src = (2, 0, 0)
task2_dest = (0, 2, 2)
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_Head(sourceAddr_tuple=task2_src, destiAddr_tuple=task2_dest))

NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())
NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_randomPayload())

NoCModel_FP_Instance.Update_injectFlit(routerAddr=task2_src, injectedFlit_tuple=SimuConfigInstance.flitGenerate_Tail())

for cnt_i in range(1, 30):
    print("Step-", cnt_i)
    NoCModel_FP_Instance.Update_oneCycle()
    NoCModel_FP_Instance.check_boundaryFlitOverflow()
    print("TASK1-DES - ", NoCModel_FP_Instance.readOut_IPReceivedFlits(routerAddr=task1_dest))
    print("TSAK2-DES - ", NoCModel_FP_Instance.readOut_IPReceivedFlits(routerAddr=task2_dest))
    print("###")

    print("Router (1.0.0) - ", NoCModel_FP_Instance.readOnly_currentRouterStates(routerAddr=(1, 0, 0)))
    print("(1.0.0)E - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 0, 0), portName="E"))
    print("(1.0.0)W - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 0, 0), portName="W"))
    print("(1.0.0)S - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 0, 0), portName="S"))
    print("(1.0.0)N - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 0, 0), portName="N"))
    print("(1.0.0)D - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 0, 0), portName="D"))
    print("(1.0.0)U - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 0, 0), portName="U"))
    print("###")
    print("Router (1.2.0) - ", NoCModel_FP_Instance.readOnly_currentRouterStates(routerAddr=(1, 2, 0)))
    print("(1.2.0)E - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 2, 0), portName="E"))
    print("(1.2.0)W - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 2, 0), portName="W"))
    print("(1.2.0)S - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 2, 0), portName="S"))
    print("(1.2.0)N - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 2, 0), portName="N"))
    print("(1.2.0)D - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 2, 0), portName="D"))
    print("(1.2.0)U - ", NoCModel_FP_Instance.readOnly_firstFlitInRouterOutFIFO(routerAddr=(1, 2, 0), portName="U"))
    print("########################################################################################################")



