//Maya ASCII 2014 scene
//Name: StartRigging.ma
//Last modified: Tue, May 19, 2015 01:10:58 PM
//Codeset: 1252
requires maya "2014";
requires -nodeType "HIKSolverNode" -nodeType "HIKRetargeterNode" -nodeType "HIKCharacterNode"
		 -nodeType "HIKSkeletonGeneratorNode" -nodeType "HIKControlSetNode" -nodeType "HIKEffectorFromCharacter"
		 -nodeType "HIKSK2State" -nodeType "HIKFK2State" -nodeType "HIKState2FK" -nodeType "HIKState2SK"
		 -nodeType "HIKState2GlobalSK" -nodeType "HIKEffector2State" -nodeType "HIKState2Effector"
		 -nodeType "HIKProperty2State" -nodeType "HIKPinning2State" -nodeType "ComputeGlobal"
		 -nodeType "ComputeLocal" -nodeType "HIKCharacterStateClient" -dataType "HIKCharacter"
		 -dataType "HIKCharacterState" -dataType "HIKEffectorState" -dataType "HIKPropertySetState"
		 "mayaHIK" "1.0_HIK_2013.2";
requires -nodeType "ilrOptionsNode" -nodeType "ilrUIOptionsNode" -nodeType "ilrBakeLayerManager"
		 -nodeType "ilrBakeLayer" -nodeType "ilrBssrdfShader" -nodeType "ilrOccSampler" -nodeType "ilrOccData"
		 -nodeType "ilrNormalMap" -nodeType "ilrSurfaceThickness" -nodeType "ilrRaySampler"
		 -nodeType "ilrBasicPhotonShader" -nodeType "ilrPhysicPhotonShader" -nodeType "ilrDielectricPhotonShader"
		 -nodeType "ilrOrenNayarShader" -nodeType "ilrAshikhminShader" -nodeType "ilrDielectricShader"
		 -nodeType "ilrLuaNode" -nodeType "ilrHwBakeVisualizer" -nodeType "ilrShadowMask"
		 -nodeType "ilrPolyColorPerVertex" -nodeType "ilrUVMappingVisualizer" -nodeType "ilrOutputShaderBackendNode"
		 -nodeType "ilrPointCloudShape" "Turtle" "2014.0.0";
requires -nodeType "mentalrayFramebuffer" -nodeType "mentalrayOutputPass" -nodeType "mentalrayRenderPass"
		 -nodeType "mentalrayUserBuffer" -nodeType "mentalraySubdivApprox" -nodeType "mentalrayCurveApprox"
		 -nodeType "mentalraySurfaceApprox" -nodeType "mentalrayDisplaceApprox" -nodeType "mentalrayOptions"
		 -nodeType "mentalrayGlobals" -nodeType "mentalrayItemsList" -nodeType "mentalrayShader"
		 -nodeType "mentalrayUserData" -nodeType "mentalrayText" -nodeType "mentalrayTessellation"
		 -nodeType "mentalrayPhenomenon" -nodeType "mentalrayLightProfile" -nodeType "mentalrayVertexColors"
		 -nodeType "mentalrayIblShape" -nodeType "mapVizShape" -nodeType "mentalrayCCMeshProxy"
		 -nodeType "cylindricalLightLocator" -nodeType "discLightLocator" -nodeType "rectangularLightLocator"
		 -nodeType "sphericalLightLocator" -nodeType "abcimport" -nodeType "mia_physicalsun"
		 -nodeType "mia_physicalsky" -nodeType "mia_material" -nodeType "mia_material_x" -nodeType "mia_roundcorners"
		 -nodeType "mia_exposure_simple" -nodeType "mia_portal_light" -nodeType "mia_light_surface"
		 -nodeType "mia_exposure_photographic" -nodeType "mia_exposure_photographic_rev" -nodeType "mia_lens_bokeh"
		 -nodeType "mia_envblur" -nodeType "mia_ciesky" -nodeType "mia_photometric_light"
		 -nodeType "mib_texture_vector" -nodeType "mib_texture_remap" -nodeType "mib_texture_rotate"
		 -nodeType "mib_bump_basis" -nodeType "mib_bump_map" -nodeType "mib_passthrough_bump_map"
		 -nodeType "mib_bump_map2" -nodeType "mib_lookup_spherical" -nodeType "mib_lookup_cube1"
		 -nodeType "mib_lookup_cube6" -nodeType "mib_lookup_background" -nodeType "mib_lookup_cylindrical"
		 -nodeType "mib_texture_lookup" -nodeType "mib_texture_lookup2" -nodeType "mib_texture_filter_lookup"
		 -nodeType "mib_texture_checkerboard" -nodeType "mib_texture_polkadot" -nodeType "mib_texture_polkasphere"
		 -nodeType "mib_texture_turbulence" -nodeType "mib_texture_wave" -nodeType "mib_reflect"
		 -nodeType "mib_refract" -nodeType "mib_transparency" -nodeType "mib_continue" -nodeType "mib_opacity"
		 -nodeType "mib_twosided" -nodeType "mib_refraction_index" -nodeType "mib_dielectric"
		 -nodeType "mib_ray_marcher" -nodeType "mib_illum_lambert" -nodeType "mib_illum_phong"
		 -nodeType "mib_illum_ward" -nodeType "mib_illum_ward_deriv" -nodeType "mib_illum_blinn"
		 -nodeType "mib_illum_cooktorr" -nodeType "mib_illum_hair" -nodeType "mib_volume"
		 -nodeType "mib_color_alpha" -nodeType "mib_color_average" -nodeType "mib_color_intensity"
		 -nodeType "mib_color_interpolate" -nodeType "mib_color_mix" -nodeType "mib_color_spread"
		 -nodeType "mib_geo_cube" -nodeType "mib_geo_torus" -nodeType "mib_geo_sphere" -nodeType "mib_geo_cone"
		 -nodeType "mib_geo_cylinder" -nodeType "mib_geo_square" -nodeType "mib_geo_instance"
		 -nodeType "mib_geo_instance_mlist" -nodeType "mib_geo_add_uv_texsurf" -nodeType "mib_photon_basic"
		 -nodeType "mib_light_infinite" -nodeType "mib_light_point" -nodeType "mib_light_spot"
		 -nodeType "mib_light_photometric" -nodeType "mib_cie_d" -nodeType "mib_blackbody"
		 -nodeType "mib_shadow_transparency" -nodeType "mib_lens_stencil" -nodeType "mib_lens_clamp"
		 -nodeType "mib_lightmap_write" -nodeType "mib_lightmap_sample" -nodeType "mib_amb_occlusion"
		 -nodeType "mib_fast_occlusion" -nodeType "mib_map_get_scalar" -nodeType "mib_map_get_integer"
		 -nodeType "mib_map_get_vector" -nodeType "mib_map_get_color" -nodeType "mib_map_get_transform"
		 -nodeType "mib_map_get_scalar_array" -nodeType "mib_map_get_integer_array" -nodeType "mib_fg_occlusion"
		 -nodeType "mib_bent_normal_env" -nodeType "mib_glossy_reflection" -nodeType "mib_glossy_refraction"
		 -nodeType "builtin_bsdf_architectural" -nodeType "builtin_bsdf_architectural_comp"
		 -nodeType "builtin_bsdf_carpaint" -nodeType "builtin_bsdf_ashikhmin" -nodeType "builtin_bsdf_lambert"
		 -nodeType "builtin_bsdf_mirror" -nodeType "builtin_bsdf_phong" -nodeType "contour_store_function"
		 -nodeType "contour_store_function_simple" -nodeType "contour_contrast_function_levels"
		 -nodeType "contour_contrast_function_simple" -nodeType "contour_shader_simple" -nodeType "contour_shader_silhouette"
		 -nodeType "contour_shader_maxcolor" -nodeType "contour_shader_curvature" -nodeType "contour_shader_factorcolor"
		 -nodeType "contour_shader_depthfade" -nodeType "contour_shader_framefade" -nodeType "contour_shader_layerthinner"
		 -nodeType "contour_shader_widthfromcolor" -nodeType "contour_shader_widthfromlightdir"
		 -nodeType "contour_shader_widthfromlight" -nodeType "contour_shader_combi" -nodeType "contour_only"
		 -nodeType "contour_composite" -nodeType "contour_ps" -nodeType "mi_metallic_paint"
		 -nodeType "mi_metallic_paint_x" -nodeType "mi_bump_flakes" -nodeType "mi_car_paint_phen"
		 -nodeType "mi_metallic_paint_output_mixer" -nodeType "mi_car_paint_phen_x" -nodeType "physical_lens_dof"
		 -nodeType "physical_light" -nodeType "dgs_material" -nodeType "dgs_material_photon"
		 -nodeType "dielectric_material" -nodeType "dielectric_material_photon" -nodeType "oversampling_lens"
		 -nodeType "path_material" -nodeType "parti_volume" -nodeType "parti_volume_photon"
		 -nodeType "transmat" -nodeType "transmat_photon" -nodeType "mip_rayswitch" -nodeType "mip_rayswitch_advanced"
		 -nodeType "mip_rayswitch_environment" -nodeType "mip_card_opacity" -nodeType "mip_motionblur"
		 -nodeType "mip_motion_vector" -nodeType "mip_matteshadow" -nodeType "mip_cameramap"
		 -nodeType "mip_mirrorball" -nodeType "mip_grayball" -nodeType "mip_gamma_gain" -nodeType "mip_render_subset"
		 -nodeType "mip_matteshadow_mtl" -nodeType "mip_binaryproxy" -nodeType "mip_rayswitch_stage"
		 -nodeType "mip_fgshooter" -nodeType "mib_ptex_lookup" -nodeType "misss_physical"
		 -nodeType "misss_physical_phen" -nodeType "misss_fast_shader" -nodeType "misss_fast_shader_x"
		 -nodeType "misss_fast_shader2" -nodeType "misss_fast_shader2_x" -nodeType "misss_skin_specular"
		 -nodeType "misss_lightmap_write" -nodeType "misss_lambert_gamma" -nodeType "misss_call_shader"
		 -nodeType "misss_set_normal" -nodeType "misss_fast_lmap_maya" -nodeType "misss_fast_simple_maya"
		 -nodeType "misss_fast_skin_maya" -nodeType "misss_fast_skin_phen" -nodeType "misss_fast_skin_phen_d"
		 -nodeType "misss_mia_skin2_phen" -nodeType "misss_mia_skin2_phen_d" -nodeType "misss_lightmap_phen"
		 -nodeType "misss_mia_skin2_surface_phen" -nodeType "surfaceSampler" -nodeType "mib_data_bool"
		 -nodeType "mib_data_int" -nodeType "mib_data_scalar" -nodeType "mib_data_vector"
		 -nodeType "mib_data_color" -nodeType "mib_data_string" -nodeType "mib_data_texture"
		 -nodeType "mib_data_shader" -nodeType "mib_data_bool_array" -nodeType "mib_data_int_array"
		 -nodeType "mib_data_scalar_array" -nodeType "mib_data_vector_array" -nodeType "mib_data_color_array"
		 -nodeType "mib_data_string_array" -nodeType "mib_data_texture_array" -nodeType "mib_data_shader_array"
		 -nodeType "mib_data_get_bool" -nodeType "mib_data_get_int" -nodeType "mib_data_get_scalar"
		 -nodeType "mib_data_get_vector" -nodeType "mib_data_get_color" -nodeType "mib_data_get_string"
		 -nodeType "mib_data_get_texture" -nodeType "mib_data_get_shader" -nodeType "mib_data_get_shader_bool"
		 -nodeType "mib_data_get_shader_int" -nodeType "mib_data_get_shader_scalar" -nodeType "mib_data_get_shader_vector"
		 -nodeType "mib_data_get_shader_color" -nodeType "user_ibl_env" -nodeType "user_ibl_rect"
		 -nodeType "mia_material_x_passes" -nodeType "mi_metallic_paint_x_passes" -nodeType "mi_car_paint_phen_x_passes"
		 -nodeType "misss_fast_shader_x_passes" -dataType "byteArray" "Mayatomr" "2014.0 - 3.11.1.9 ";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2014";
fileInfo "version" "2014";
fileInfo "cutIdentifier" "201307170459-880822";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 25.957992320533055 14.108768194045783 56.469996962418833 ;
	setAttr ".r" -type "double3" -9.3383527298602722 22.999999999980854 4.3190357301404965e-016 ;
	setAttr ".rp" -type "double3" -7.5495165674510645e-015 2.6645352591003757e-015 0 ;
	setAttr ".rpt" -type "double3" 1.1742911875419935e-014 1.1580632828523174e-014 1.622343898122399e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999979;
	setAttr ".coi" 63.589549415457206;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -2.6314108385478372 148.73989662799985 100.11927876371594 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 97.146778648522073;
	setAttr ".ow" 229.18097830065574;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".tp" -type "double3" -4.1392341041125906 149.44354748526339 2.972500115193867 ;
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "Lucas_Reference";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
createNode locator -n "Lucas_ReferenceShape" -p "Lucas_Reference";
	setAttr -k off ".v";
createNode joint -n "Lucas_Hips" -p "Lucas_Reference";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0 100 0 ;
	setAttr ".jo" -type "double3" 0 0 -35.134192611069459 ;
	setAttr ".ssc" no;
	setAttr ".typ" 1;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftUpLeg" -p "Lucas_Hips";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 10.89499977247457 0 0 ;
	setAttr ".jo" -type "double3" 82.522507629330335 -6.8133726889364947 -168.0343625996023 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 2;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftLeg" -p "Lucas_LeftUpLeg";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -17.533953004540862 12.765636527170727 -39.660294858755243 ;
	setAttr ".jo" -type "double3" -46.091164120594819 -10.067268597345022 165.16170461037538 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 3;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftFoot" -p "Lucas_LeftLeg";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 8.8806103470013458 30.677861412102143 -25.803464540621629 ;
	setAttr ".jo" -type "double3" 84.777275600315335 31.127894074813245 -53.335400100107449 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 4;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftToeBase" -p "Lucas_LeftFoot";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 6.6608416276537206 -6.1069493583700858 -2.0725807259564593 ;
	setAttr ".jo" -type "double3" 105.06036864235756 -19.839074474198963 39.049558097108402 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 5;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftFootMiddle1" -p "Lucas_LeftToeBase";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 2.8201203674647743 1.1959591663483033 3.001685577907331 ;
	setAttr ".jo" -type "double3" 79.043982325131367 63.333985769094063 176.79167183659945 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 26;
createNode joint -n "Lucas_LeftFootMiddle2" -p "Lucas_LeftFootMiddle1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -4.4822229760400027 -1.539184163641341 1.2855863835902221 ;
	setAttr ".jo" -type "double3" -107.93378105452776 57.440018710498983 -102.33842274208088 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 26;
createNode joint -n "Lucas_RightUpLeg" -p "Lucas_Hips";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -3.6783120093923785 -10.255293306570053 0 ;
	setAttr ".jo" -type "double3" 89.999999999999957 -5.425348448994467 -168.92645911144436 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 2;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_RightLeg" -p "Lucas_RightUpLeg";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -17.072930670050177 7.0083483306133498 -41.26424680283332 ;
	setAttr ".jo" -type "double3" -53.971230717810926 12.922969665343798 146.57954781784451 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 3;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_RightFoot" -p "Lucas_RightLeg";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 20.624602796281049 34.316212938863572 -9.1015653755132071 ;
	setAttr ".jo" -type "double3" -21.482427470612354 -55.566947241253274 108.40211415415823 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 4;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_RightToeBase" -p "Lucas_RightFoot";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -6.1558754135960259 -5.1252239675925777 -4.6684590278041664 ;
	setAttr ".jo" -type "double3" -69.896760531974408 -57.244645620553754 -160.84987620597857 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 5;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_RightFootMiddle1" -p "Lucas_RightToeBase";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 2.728716528522003 3.0767567963881151 -1.2170403633525986 ;
	setAttr ".jo" -type "double3" 12.513093810485467 21.71474579374058 -23.671452349192997 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 26;
createNode joint -n "Lucas_RightFootMiddle2" -p "Lucas_RightFootMiddle1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 1.8596121937077701 4.2127648610939197 -1.7048747051802433 ;
	setAttr ".jo" -type "double3" 22.195611240551923 11.444985261814127 -91.743537732234685 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 26;
createNode joint -n "Lucas_Spine" -p "Lucas_Hips";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -25.416617100518401 36.118351213698176 0 ;
	setAttr ".jo" -type "double3" 0 0 -109.04253187300282 ;
	setAttr ".ssc" no;
	setAttr ".typ" 6;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftShoulder" -p "Lucas_Spine";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -7.0943036755838023 2.1318660872162525 0 ;
	setAttr ".jo" -type "double3" 0 0 113.76492079920989 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 9;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftArm" -p "Lucas_LeftShoulder";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 9.2339640198937261 5.4202512635012283 0 ;
	setAttr ".jo" -type "double3" 1.3585323626560095 10.933297019161015 38.642007221790763 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 10;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftForeArm" -p "Lucas_LeftArm";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 28.021805804668048 -0.52963506494143076 0.01159292978191262 ;
	setAttr ".jo" -type "double3" -39.698722135412979 -23.485520917557963 122.03385742356367 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 11;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftHand" -p "Lucas_LeftForeArm";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -13.199795357009023 -23.951818988300246 2.1742213638402887 ;
	setAttr ".jo" -type "double3" -100.73802301308197 -76.183997094783194 -115.61409083556042 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 12;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_LeftHandThumb1" -p "Lucas_LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 4.1890601779058301 3.7620052859718243 2.4874935414683677 ;
	setAttr ".jo" -type "double3" 86.944508452037724 -37.829338024993987 -41.191188199754983 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 14;
createNode joint -n "Lucas_LeftHandThumb2" -p "Lucas_LeftHandThumb1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.42511805199164954 0.813692291429021 -2.5016358429147569 ;
	setAttr ".jo" -type "double3" 145.68550887455535 60.41203088647795 -46.008433357560563 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 14;
createNode joint -n "Lucas_LeftHandThumb3" -p "Lucas_LeftHandThumb2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.94150516887611957 -1.4230902189026153 1.8857214510844109 ;
	setAttr ".jo" -type "double3" 115.06421486415061 -15.755241904463785 149.17379069993603 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 14;
createNode joint -n "Lucas_LeftHandThumb4" -p "Lucas_LeftHandThumb3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -1.0149635558624226 1.7919387565704668 -1.6942076166315303 ;
	setAttr ".jo" -type "double3" -57.02923740557975 -16.061948057083995 -40.997781358713041 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 14;
createNode joint -n "Lucas_LeftHandIndex1" -p "Lucas_LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 3.3331045463459787 8.2815510974871103 3.1978084743117989 ;
	setAttr ".jo" -type "double3" 87.089312165814604 33.993759043558832 -44.694601296632996 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 19;
createNode joint -n "Lucas_LeftHandIndex2" -p "Lucas_LeftHandIndex1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -2.4257251848605108 -0.85077433045785256 -3.3534108501155391 ;
	setAttr ".jo" -type "double3" -162.54020648016873 -11.764502651854691 -106.25578670343249 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 19;
createNode joint -n "Lucas_LeftHandIndex3" -p "Lucas_LeftHandIndex2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.49032207184422028 1.928773039391757 1.7557896313406047 ;
	setAttr ".jo" -type "double3" 81.599303910816744 -32.691466007164742 -8.7452861968446385 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 19;
createNode joint -n "Lucas_LeftHandIndex4" -p "Lucas_LeftHandIndex3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.81856366334243802 1.2166882400237409 -1.2977904497481347 ;
	setAttr ".jo" -type "double3" -49.63265718809641 -64.187903015513285 -150.75873363182029 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 19;
createNode joint -n "Lucas_LeftHandMiddle1" -p "Lucas_LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 1.4736605775586611 8.548925237357281 2.0763594951246489 ;
	setAttr ".jo" -type "double3" 87.089312165814604 33.993759043558832 -44.694601296632996 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 20;
createNode joint -n "Lucas_LeftHandMiddle2" -p "Lucas_LeftHandMiddle1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -2.8243508102517865 -1.1316387218477786 -3.7938968486696929 ;
	setAttr ".jo" -type "double3" -162.54032067870838 -11.762759153295242 -106.25522656252411 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 20;
createNode joint -n "Lucas_LeftHandMiddle3" -p "Lucas_LeftHandMiddle2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.60507062028779579 1.9978017655768099 1.813618258817435 ;
	setAttr ".jo" -type "double3" 81.604913696353961 -32.684973018717038 -8.7526011037523546 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 20;
createNode joint -n "Lucas_LeftHandMiddle4" -p "Lucas_LeftHandMiddle3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.8898406293982859 1.2001749553948713 -1.3380299350978078 ;
	setAttr ".jo" -type "double3" -49.601387618588774 -64.196905946648457 -150.7580981602722 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 20;
createNode joint -n "Lucas_LeftHandRing1" -p "Lucas_LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.057169794740374869 8.9109980339491983 0.68062384114257668 ;
	setAttr ".jo" -type "double3" 87.089312165814604 33.993759043558832 -44.694601296632996 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 21;
createNode joint -n "Lucas_LeftHandRing2" -p "Lucas_LeftHandRing1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -2.6353708174281678 -1.0561523354462068 -3.5398613105916485 ;
	setAttr ".jo" -type "double3" -162.54032067870838 -11.762759153295242 -106.25522656252411 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 21;
createNode joint -n "Lucas_LeftHandRing3" -p "Lucas_LeftHandRing2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.50440067038414682 1.6649323658739092 1.5114296610130964 ;
	setAttr ".jo" -type "double3" 81.604913696353961 -32.684973018717038 -8.7526011037523546 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 21;
createNode joint -n "Lucas_LeftHandRing4" -p "Lucas_LeftHandRing3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.85342082083631254 1.1508555791659987 -1.2831482399493552 ;
	setAttr ".jo" -type "double3" -49.601387618588774 -64.196905946648457 -150.7580981602722 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 21;
createNode joint -n "Lucas_LeftHandPinky1" -p "Lucas_LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.92657240843720956 9.1375351173798975 -0.9173769370779894 ;
	setAttr ".jo" -type "double3" 87.089312165814604 33.993759043558832 -44.694601296632996 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 22;
createNode joint -n "Lucas_LeftHandPinky2" -p "Lucas_LeftHandPinky1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -1.7679381170613055 -0.70849153597281855 -2.3746526672867256 ;
	setAttr ".jo" -type "double3" -162.54032067870838 -11.762759153295242 -106.25522656252411 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 22;
createNode joint -n "Lucas_LeftHandPinky3" -p "Lucas_LeftHandPinky2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.43216598707325815 1.4265201217074832 1.2949629479964671 ;
	setAttr ".jo" -type "double3" 81.604913696353961 -32.684973018717038 -8.7526011037523546 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 22;
createNode joint -n "Lucas_LeftHandPinky4" -p "Lucas_LeftHandPinky3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.73949177649521403 0.99722805099411893 -1.1118869182138553 ;
	setAttr ".jo" -type "double3" -49.601387618588774 -64.196905946648457 -150.7580981602722 ;
	setAttr ".ssc" no;
	setAttr ".sd" 1;
	setAttr ".typ" 22;
createNode joint -n "Lucas_RightShoulder" -p "Lucas_Spine";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 4.2572628080339996 -6.0621539933059125 0 ;
	setAttr ".jo" -type "double3" 0 0 113.76492079920989 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 9;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_RightArm" -p "Lucas_RightShoulder";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -9.2341031267980753 -5.4200142733978538 0 ;
	setAttr ".jo" -type "double3" 178.64146763734399 10.933297019161076 -155.61221849627708 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 10;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_RightForeArm" -p "Lucas_RightArm";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 28.021805804668055 0.52958920026642886 0.013526899037857643 ;
	setAttr ".jo" -type "double3" -156.05607077571278 -20.916511187598104 43.930546533665115 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 11;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_RightHand" -p "Lucas_RightForeArm";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 9.0747973345468154 25.48168813982538 4.5807304805872775 ;
	setAttr ".jo" -type "double3" 43.349476774563563 55.427184345308341 22.144260474254981 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 12;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_RightHandThumb1" -p "Lucas_RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -2.0019253942519804 5.7635116203316628 -0.81410170297962736 ;
	setAttr ".jo" -type "double3" -14.143215185739152 36.963772863592794 59.894099048129888 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 14;
createNode joint -n "Lucas_RightHandThumb2" -p "Lucas_RightHandThumb1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 2.1885373421936976 0.59161232508386163 1.4004647630157194 ;
	setAttr ".jo" -type "double3" -170.34197255632242 20.139292411158664 49.259154553438862 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 14;
createNode joint -n "Lucas_RightHandThumb3" -p "Lucas_RightHandThumb2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.42331833197728486 1.1449973593325424 -2.2309965894572485 ;
	setAttr ".jo" -type "double3" -4.2896279448032084 67.74147836349735 -149.46226431642106 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 14;
createNode joint -n "Lucas_RightHandThumb4" -p "Lucas_RightHandThumb3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 1.7892165694762241 -0.67133988567336544 -1.8599843549601047 ;
	setAttr ".jo" -type "double3" -122.11324446811993 9.4055033807564623 -60.993176780563005 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 14;
createNode joint -n "Lucas_RightHandIndex1" -p "Lucas_RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.38838521993045561 9.4464319135541572 0.73057139217723943 ;
	setAttr ".jo" -type "double3" -39.213046177044284 0.073247472877887659 -7.2803420073408835 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 19;
createNode joint -n "Lucas_RightHandIndex2" -p "Lucas_RightHandIndex1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 1.060980834282977 2.8822449848601721 2.9017766075350266 ;
	setAttr ".jo" -type "double3" -164.04599316587462 44.624997928192926 -2.9684558651065718 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 19;
createNode joint -n "Lucas_RightHandIndex3" -p "Lucas_RightHandIndex2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.87338765596526002 -2.2384135113137882 -1.1269770875757814 ;
	setAttr ".jo" -type "double3" 79.592390610011748 45.487142713995723 93.978534364862938 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 19;
createNode joint -n "Lucas_RightHandIndex4" -p "Lucas_RightHandIndex3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.53079735267272099 -1.5607782748981762 -1.0568169864341002 ;
	setAttr ".jo" -type "double3" 52.241836570279155 -87.604457142391439 89.2032851282639 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 19;
createNode joint -n "Lucas_RightHandMiddle1" -p "Lucas_RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 2.2980954164443865 8.5249116636113271 1.2695296567272294 ;
	setAttr ".jo" -type "double3" -39.213046177044284 0.073247472877887659 -7.2803420073408835 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 20;
createNode joint -n "Lucas_RightHandMiddle2" -p "Lucas_RightHandMiddle1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 1.3824335682724975 3.2685511134118599 3.3251568448464184 ;
	setAttr ".jo" -type "double3" -164.04599316587462 44.624997928192926 -2.9684558651065718 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 20;
createNode joint -n "Lucas_RightHandMiddle3" -p "Lucas_RightHandMiddle2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.83793553853863045 -2.3265036017514991 -1.2376504203870979 ;
	setAttr ".jo" -type "double3" 79.592390610011748 45.487142713995723 93.978534364862938 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 20;
createNode joint -n "Lucas_RightHandMiddle4" -p "Lucas_RightHandMiddle3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.51046042042401041 -1.6393615558307673 -1.0365733090078351 ;
	setAttr ".jo" -type "double3" 52.241836570279155 -87.604457142391439 89.2032851282639 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 20;
createNode joint -n "Lucas_RightHandRing1" -p "Lucas_RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 4.2452010094302999 7.7400570689702519 1.3936240950214938 ;
	setAttr ".jo" -type "double3" -39.213046177044284 0.073247472877887659 -7.2803420073408835 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 21;
createNode joint -n "Lucas_RightHandRing2" -p "Lucas_RightHandRing1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 1.2901762214247663 3.0497052961208553 3.1025792695315033 ;
	setAttr ".jo" -type "double3" -164.04599316587462 44.624997928192926 -2.9684558651065718 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 21;
createNode joint -n "Lucas_RightHandRing3" -p "Lucas_RightHandRing2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.69822054246220944 -1.9388786031525669 -1.0315412137812814 ;
	setAttr ".jo" -type "double3" 79.592390610011748 45.487142713995723 93.978534364862938 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 21;
createNode joint -n "Lucas_RightHandRing4" -p "Lucas_RightHandRing3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.48946052780642901 -1.5721717946480567 -0.99396645167341546 ;
	setAttr ".jo" -type "double3" 52.241836570279155 -87.604457142391439 89.2032851282639 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 21;
createNode joint -n "Lucas_RightHandPinky1" -p "Lucas_RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 5.8747588060317781 7.0622988065064689 0.89766888810947876 ;
	setAttr ".jo" -type "double3" -39.213046177044284 0.073247472877887659 -7.2803420073408835 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 22;
createNode joint -n "Lucas_RightHandPinky2" -p "Lucas_RightHandPinky1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" 0.86549316468192661 2.045829544964775 2.0813562375032859 ;
	setAttr ".jo" -type "double3" -164.04599316587462 44.624997928192926 -2.9684558651065718 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 22;
createNode joint -n "Lucas_RightHandPinky3" -p "Lucas_RightHandPinky2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.59824569608164779 -1.6612034192118657 -0.88383336767824972 ;
	setAttr ".jo" -type "double3" 79.592390610011748 45.487142713995723 93.978534364862938 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 22;
createNode joint -n "Lucas_RightHandPinky4" -p "Lucas_RightHandPinky3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -0.42410832481196792 -1.3623121846777835 -0.86130252083241032 ;
	setAttr ".jo" -type "double3" 52.241836570279155 -87.604457142391439 89.2032851282639 ;
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr ".typ" 22;
createNode joint -n "Lucas_Neck" -p "Lucas_Spine";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -5.7398686696220409 -7.9517135874897349 0 ;
	setAttr ".jo" -type "double3" 0 0 113.76492079920989 ;
	setAttr ".ssc" no;
	setAttr ".typ" 7;
	setAttr ".radi" 3.0000000000000013;
createNode joint -n "Lucas_Head" -p "Lucas_Neck";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".t" -type "double3" -5.582579133853784 9.5107860545294614 0 ;
	setAttr ".jo" -type "double3" 0 0 154.76789262584398 ;
	setAttr ".ssc" no;
	setAttr ".typ" 8;
	setAttr ".radi" 3.0000000000000013;
createNode transform -n "c_eye_ctrl";
	addAttr -ci true -sn "followHead" -ln "followHead" -min 0 -max 1 -at "double";
	setAttr ".t" -type "double3" 0 -6.2172489379008774e-015 0 ;
	setAttr ".s" -type "double3" 3.1952367855135848 3.1952367855135848 3.1952367855135848 ;
	setAttr ".rp" -type "double3" -8.8817841970012523e-016 15.85509911705371 7.5382055086899022 ;
	setAttr ".sp" -type "double3" -8.8817841970012523e-016 15.85509911705371 7.5382055086899022 ;
	setAttr -k on ".followHead" 1;
createNode nurbsCurve -n "c_eye_ctrlShape" -p "c_eye_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 10 2 no 3
		15 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12
		13
		1.2004104257731931 17.027771135180497 7.5382055086899022
		-5.5082388781043376e-016 16.306140797331004 7.5382055086899022
		-1.2004104257731962 17.027771135180497 7.5382055086899022
		-2.3433269071248777 16.417826406114482 7.5382055086899022
		-2.343326907124879 15.292371827992936 7.5382055086899022
		-1.2004104257731962 14.682427098926921 7.5382055086899022
		-9.9498607345547852e-016 15.404057436776414 7.5382055086899022
		1.200410425773194 14.682427098926921 7.5382055086899022
		2.3433269071248768 15.292371827992936 7.5382055086899022
		2.3433269071248772 16.417826406114482 7.5382055086899022
		1.2004104257731931 17.027771135180497 7.5382055086899022
		-5.5082388781043376e-016 16.306140797331004 7.5382055086899022
		-1.2004104257731962 17.027771135180497 7.5382055086899022
		;
createNode transform -n "l_eye_ctrl" -p "c_eye_ctrl";
	setAttr ".rp" -type "double3" 1.3362541721146022 15.855099117053712 7.5382055086899005 ;
	setAttr ".sp" -type "double3" 1.3362541721146022 15.855099117053712 7.5382055086899005 ;
createNode nurbsCurve -n "l_eye_ctrlShape" -p "l_eye_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 4 2 no 3
		9 -2 -1 0 1 2 3 4 5 6
		7
		2.0712541721146023 15.855099117053712 7.5382055086899005
		1.3362541721146022 16.590099117053711 7.5382055086899005
		0.6012541721146023 15.855099117053712 7.5382055086899005
		1.336254172114602 15.120099117053712 7.5382055086899005
		2.0712541721146023 15.855099117053712 7.5382055086899005
		1.3362541721146022 16.590099117053711 7.5382055086899005
		0.6012541721146023 15.855099117053712 7.5382055086899005
		;
createNode transform -n "r_eye_ctrl" -p "c_eye_ctrl";
	setAttr ".rp" -type "double3" -1.336254172114604 15.855099117053708 7.5382055086899031 ;
	setAttr ".sp" -type "double3" -1.336254172114604 15.855099117053708 7.5382055086899031 ;
createNode nurbsCurve -n "r_eye_ctrlShape" -p "r_eye_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 4 2 no 3
		9 -2 -1 0 1 2 3 4 5 6
		7
		-0.60125417211460408 15.855099117053708 7.5382055086899031
		-1.336254172114604 16.590099117053708 7.5382055086899031
		-2.0712541721146041 15.855099117053708 7.5382055086899031
		-1.3362541721146042 15.120099117053709 7.5382055086899031
		-0.60125417211460408 15.855099117053708 7.5382055086899031
		-1.336254172114604 16.590099117053708 7.5382055086899031
		-2.0712541721146041 15.855099117053708 7.5382055086899031
		;
createNode transform -n "ControlCross";
	addAttr -ci true -sn "js_up" -ln "js_up" -at "message";
	addAttr -ci true -sn "js_down" -ln "js_down" -at "message";
	addAttr -ci true -sn "objectName" -ln "objectName" -dt "string";
	setAttr ".objectName" -type "string" "Spine2";
createNode nurbsCurve -n "ControlCrossShape" -p "ControlCross";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 28;
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		0 0 -0.49460736640257613
		-2.7456224316467555e-017 -0.12365184160064403 -0.32973824426838405
		-9.1520747721558507e-018 -0.041217280533548006 -0.32973824426838405
		-9.1520747721558507e-018 -0.041217280533548006 -0.041217280533548006
		-7.3216598177246806e-017 -0.32973824426838405 -0.041217280533548006
		-7.3216598177246806e-017 -0.32973824426838405 -0.12365184160064403
		-1.0982489726587022e-016 -0.49460736640257613 0
		-7.3216598177246806e-017 -0.32973824426838405 0.12365184160064403
		-7.3216598177246806e-017 -0.32973824426838405 0.041217280533548006
		-9.1520747721558507e-018 -0.041217280533548006 0.041217280533548006
		-9.1520747721558507e-018 -0.041217280533548006 0.32973824426838405
		-2.7456224316467555e-017 -0.12365184160064403 0.32973824426838405
		0 0 0.49460736640257613
		2.7456224316467555e-017 0.12365184160064403 0.32973824426838405
		9.1520747721558507e-018 0.041217280533548006 0.32973824426838405
		9.1520747721558507e-018 0.041217280533548006 0.041217280533548006
		7.3216598177246806e-017 0.32973824426838405 0.041217280533548006
		7.3216598177246806e-017 0.32973824426838405 0.12365184160064403
		1.0982489726587022e-016 0.49460736640257613 0
		7.3216598177246806e-017 0.32973824426838405 -0.12365184160064403
		7.3216598177246806e-017 0.32973824426838405 -0.041217280533548006
		9.1520747721558507e-018 0.041217280533548006 -0.041217280533548006
		9.1520747721558507e-018 0.041217280533548006 -0.32973824426838405
		2.7456224316467555e-017 0.12365184160064403 -0.32973824426838405
		0 0 -0.49460736640257613
		;
createNode transform -n "ControlCabeza";
	addAttr -ci true -sn "AlignedTo" -ln "AlignedTo" -min 0 -max 1 -en "World:Neck" 
		-at "enum";
	setAttr ".ro" 2;
	setAttr -k on ".AlignedTo";
createNode nurbsCurve -n "ControlCabezaShape" -p "ControlCabeza";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 25;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32
		33
		0.40485415870381841 8.7156419949855821e-017 0.61523327025662045
		0.68877397793298656 1.5019928404098277e-016 0.62947729596732882
		0.93036416466987915 2.0384308160874062e-016 0.34560319373039561
		0.99963355482937333 2.1922397598010336e-016 0.037477083045614541
		0.9430997006081574 2.0667093865466416e-016 -0.28762974222353688
		0.71424504980954184 1.5585499813282956e-016 -0.5144833590819462
		0.40126288359011003 8.6358996686055347e-017 -0.5830203169700412
		0.10526143195504767 2.0633471300512162e-017 -0.47415416194406762
		-0.11298027222833579 -2.782592168305277e-017 -0.25791349170088945
		-0.19286260900306101 -4.5563363592684932e-017 0.037477083045614541
		-0.27429706077985067 -6.3645444264748704e-017 0.50267480363581729
		0.16316097340076563 3.3489752106167083e-017 0.70405734861767089
		0.40485415870381841 8.7156419949855821e-017 0.61523327025662045
		0.40338547291315624 -0.37347218157122947 0.45522256932016625
		0.4033854729131563 -0.52816926090567573 0.037477083045614541
		0.40338547291315624 -0.37347218157122947 -0.38026840322893796
		0.40126288359011003 8.6358996686055347e-017 -0.5830203169700412
		0.40338547291315613 0.37347218157122969 -0.38026840322893796
		0.40338547291315607 0.52816926090567595 0.037477083045614541
		0.7015095138712647 0.4792410267080926 0.037477083045614541
		0.91975121805464821 0.27669006478340286 0.037477083045614541
		0.99963355482937333 2.1922397598010336e-016 0.037477083045614541
		0.91975121805464843 -0.27669006478340241 0.037477083045614541
		0.70150951387126492 -0.47924102670809227 0.037477083045614541
		0.4033854729131563 -0.52816926090567573 0.037477083045614541
		0.10526143195504777 -0.45740778417583772 0.037477083045614541
		-0.11298027222833573 -0.26408463045283792 0.037477083045614541
		-0.19286260900306101 -4.5563363592684932e-017 0.037477083045614541
		-0.11298027222833584 0.26408463045283792 0.037477083045614541
		0.10526143195504757 0.45740778417583772 0.037477083045614541
		0.40338547291315607 0.52816926090567595 0.037477083045614541
		0.40338547291315613 0.37347218157122969 0.45522256932016625
		0.40485415870381841 8.7156419949855821e-017 0.61523327025662045
		;
createNode transform -n "clav_ctrl";
createNode nurbsCurve -n "curveShape1" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 -0.5 0.5
		0 -0.5 -0.5
		;
createNode nurbsCurve -n "curveShape2" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		1 -0.5 0.5
		1 -0.5 -0.5
		;
createNode nurbsCurve -n "curveShape3" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0.5 0.5
		0 0.5 -0.5
		;
createNode nurbsCurve -n "curveShape4" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0.79721353964466424 0.5 0.5
		0.79721353964466424 0.5 -0.5
		;
createNode nurbsCurve -n "curveShape5" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 -0.5 0.5
		1 -0.5 0.5
		;
createNode nurbsCurve -n "curveShape6" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0.5 -0.5
		0.79721353964466424 0.5 -0.5
		;
createNode nurbsCurve -n "curveShape7" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 -0.5 -0.5
		1 -0.5 -0.5
		;
createNode nurbsCurve -n "curveShape8" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0.5 0.5
		0.79721353964466424 0.5 0.5
		;
createNode nurbsCurve -n "curveShape9" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 -0.5 -0.5
		0 0.5 -0.5
		;
createNode nurbsCurve -n "curveShape10" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 -0.5 0.5
		0 0.5 0.5
		;
createNode nurbsCurve -n "curveShape11" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		1 -0.5 -0.5
		0.79721353964466424 0.5 -0.5
		;
createNode nurbsCurve -n "curveShape12" -p "clav_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		1 -0.5 0.5
		0.79721353964466424 0.5 0.5
		;
createNode transform -n "V";
createNode nurbsCurve -n "VShape" -p "V";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 7 2 no 3
		8 0 0.099999999999999978 2.6632011235952597 2.96320112359526 4.7832288683939499
		 6.6032560682357984 6.9032560682357982 9.4664571918310578
		8
		0.020123735668005349 0 0
		-0.020123735668005516 0 0
		-0.38235097769210363 0.96593931206426165 0
		-0.26160856368407093 0.96593931206426165 0
		3.070685231643111e-007 0.28173229935207633 0
		0.26160856368407076 0.96593931206426165 0
		0.38235097769210363 0.96593931206426165 0
		0.020123735668005349 0 0
		;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode HIKCharacterNode -n "Lucas";
	setAttr ".OutputCharacterDefinition" -type "HIKCharacter" ;
	setAttr ".ReferenceMinRLimitx" -45;
	setAttr ".ReferenceMinRLimity" -45;
	setAttr ".ReferenceMinRLimitz" -45;
	setAttr ".ReferenceMaxRLimitx" 45;
	setAttr ".ReferenceMaxRLimity" 45;
	setAttr ".ReferenceMaxRLimitz" 45;
	setAttr ".HipsTy" 100;
	setAttr ".HipsRz" -35.134192611069459;
	setAttr ".HipsJointOrientz" -35.134192611069459;
	setAttr ".HipsMinRLimitx" -45;
	setAttr ".HipsMinRLimity" -45;
	setAttr ".HipsMinRLimitz" -45;
	setAttr ".HipsMaxRLimitx" 45;
	setAttr ".HipsMaxRLimity" 45;
	setAttr ".HipsMaxRLimitz" 45;
	setAttr ".LeftUpLegTx" 8.9100008010000025;
	setAttr ".LeftUpLegTy" 93.729999539999994;
	setAttr ".LeftUpLegRx" 82.522507629330349;
	setAttr ".LeftUpLegRy" -6.8133726889364974;
	setAttr ".LeftUpLegRz" 156.83144478932829;
	setAttr ".LeftUpLegJointOrientx" 82.522507629330335;
	setAttr ".LeftUpLegJointOrienty" -6.8133726889364947;
	setAttr ".LeftUpLegJointOrientz" -168.03436259960233;
	setAttr ".LeftUpLegMinRLimitx" -45;
	setAttr ".LeftUpLegMinRLimity" -45;
	setAttr ".LeftUpLegMinRLimitz" -45;
	setAttr ".LeftUpLegMaxRLimitx" 45;
	setAttr ".LeftUpLegMaxRLimity" 45;
	setAttr ".LeftUpLegMaxRLimitz" 45;
	setAttr ".LeftLegTx" 9.6088187334525159;
	setAttr ".LeftLegTy" 48.851354599999866;
	setAttr ".LeftLegTz" 5.3627282272528465;
	setAttr ".LeftLegRx" -130.09199081353464;
	setAttr ".LeftLegRy" -9.0857840586908019;
	setAttr ".LeftLegRz" -14.988219651530052;
	setAttr ".LeftLegSz" 0.99999999999999989;
	setAttr ".LeftLegJointOrientx" -46.091164120594819;
	setAttr ".LeftLegJointOrienty" -10.067268597345022;
	setAttr ".LeftLegJointOrientz" 165.16170461037538;
	setAttr ".LeftLegMinRLimitx" -45;
	setAttr ".LeftLegMinRLimity" -45;
	setAttr ".LeftLegMinRLimitz" -45;
	setAttr ".LeftLegMaxRLimitx" 45;
	setAttr ".LeftLegMaxRLimity" 45;
	setAttr ".LeftLegMaxRLimitz" 45;
	setAttr ".LeftFootTx" 8.9100008010000771;
	setAttr ".LeftFootTy" 8.1503963469999832;
	setAttr ".LeftFootTz" -5.3290705182007514e-015;
	setAttr ".LeftFootRx" -34.566890927544932;
	setAttr ".LeftFootRy" -68.15100416306916;
	setAttr ".LeftFootRz" -7.773322154255645;
	setAttr ".LeftFootSy" 0.99999999999999989;
	setAttr ".LeftFootJointOrientx" 84.777275600315335;
	setAttr ".LeftFootJointOrienty" 31.127894074813245;
	setAttr ".LeftFootJointOrientz" -53.335400100107449;
	setAttr ".LeftFootMinRLimitx" -45;
	setAttr ".LeftFootMinRLimity" -45;
	setAttr ".LeftFootMinRLimitz" -45;
	setAttr ".LeftFootMaxRLimitx" 45;
	setAttr ".LeftFootMaxRLimity" 45;
	setAttr ".LeftFootMaxRLimitz" 45;
	setAttr ".RightUpLegTx" -8.9100008009999971;
	setAttr ".RightUpLegTy" 93.729999540000009;
	setAttr ".RightUpLegRx" 90;
	setAttr ".RightUpLegRy" -5.425348448994467;
	setAttr ".RightUpLegRz" 155.93934827748618;
	setAttr ".RightUpLegSx" 1.0000000000000002;
	setAttr ".RightUpLegJointOrientx" 89.999999999999957;
	setAttr ".RightUpLegJointOrienty" -5.425348448994467;
	setAttr ".RightUpLegJointOrientz" -168.92645911144436;
	setAttr ".RightUpLegMinRLimitx" -45;
	setAttr ".RightUpLegMinRLimity" -45;
	setAttr ".RightUpLegMinRLimitz" -45;
	setAttr ".RightUpLegMaxRLimitx" 45;
	setAttr ".RightUpLegMaxRLimity" 45;
	setAttr ".RightUpLegMaxRLimitz" 45;
	setAttr ".RightLegTx" -9.6088187334525212;
	setAttr ".RightLegTy" 48.85135459999988;
	setAttr ".RightLegTz" 5.3627282272528474;
	setAttr ".RightLegRx" -137.19130509550169;
	setAttr ".RightLegRy" -27.226359454688808;
	setAttr ".RightLegRz" -38.627314795645432;
	setAttr ".RightLegSx" 1.0000000000000002;
	setAttr ".RightLegSy" 0.99999999999999989;
	setAttr ".RightLegSz" 1.0000000000000002;
	setAttr ".RightLegJointOrientx" -53.971230717810926;
	setAttr ".RightLegJointOrienty" 12.922969665343798;
	setAttr ".RightLegJointOrientz" 146.57954781784451;
	setAttr ".RightLegMinRLimitx" -45;
	setAttr ".RightLegMinRLimity" -45;
	setAttr ".RightLegMinRLimitz" -45;
	setAttr ".RightLegMaxRLimitx" 45;
	setAttr ".RightLegMaxRLimity" 45;
	setAttr ".RightLegMaxRLimitz" 45;
	setAttr ".RightFootTx" -8.9100008010000771;
	setAttr ".RightFootTy" 8.1503963469999761;
	setAttr ".RightFootTz" -1.3322676295501878e-014;
	setAttr ".RightFootRx" -68.961213134681969;
	setAttr ".RightFootRy" 70.719923053033469;
	setAttr ".RightFootRz" -8.2696792435262214;
	setAttr ".RightFootSx" 1.0000000000000004;
	setAttr ".RightFootSy" 1.0000000000000004;
	setAttr ".RightFootSz" 0.99999999999999989;
	setAttr ".RightFootJointOrientx" -21.482427470612354;
	setAttr ".RightFootJointOrienty" -55.566947241253281;
	setAttr ".RightFootJointOrientz" 108.40211415415823;
	setAttr ".RightFootMinRLimitx" -45;
	setAttr ".RightFootMinRLimity" -45;
	setAttr ".RightFootMinRLimitz" -45;
	setAttr ".RightFootMaxRLimitx" 45;
	setAttr ".RightFootMaxRLimity" 45;
	setAttr ".RightFootMaxRLimitz" 45;
	setAttr ".SpineTx" -7.1054273576010019e-015;
	setAttr ".SpineTy" 144.16491502573527;
	setAttr ".SpineRz" -144.17672448407225;
	setAttr ".SpineJointOrientz" -109.04253187300282;
	setAttr ".SpineMinRLimitx" -45;
	setAttr ".SpineMinRLimity" -45;
	setAttr ".SpineMinRLimitz" -45;
	setAttr ".SpineMaxRLimitx" 45;
	setAttr ".SpineMaxRLimity" 45;
	setAttr ".SpineMaxRLimitz" 45;
	setAttr ".LeftArmTx" 17.707251069999948;
	setAttr ".LeftArmTy" 146.58868419999993;
	setAttr ".LeftArmRx" 1.3585323626560097;
	setAttr ".LeftArmRy" 10.933297019161015;
	setAttr ".LeftArmRz" 8.2302035369283981;
	setAttr ".LeftArmJointOrientx" 1.3585323626560095;
	setAttr ".LeftArmJointOrienty" 10.933297019161015;
	setAttr ".LeftArmJointOrientz" 38.642007221790763;
	setAttr ".LeftArmMinRLimitx" -45;
	setAttr ".LeftArmMinRLimity" -45;
	setAttr ".LeftArmMinRLimitz" -45;
	setAttr ".LeftArmMaxRLimitx" 45;
	setAttr ".LeftArmMaxRLimity" 45;
	setAttr ".LeftArmMaxRLimitz" 45;
	setAttr ".LeftForeArmTx" 45.012716769999912;
	setAttr ".LeftForeArmTy" 150.00288216303824;
	setAttr ".LeftForeArmTz" -5.3157354550311018;
	setAttr ".LeftForeArmRx" -29.819049826449788;
	setAttr ".LeftForeArmRy" -30.102048693666571;
	setAttr ".LeftForeArmRz" 125.66422333797445;
	setAttr ".LeftForeArmSx" 0.99999999999999978;
	setAttr ".LeftForeArmJointOrientx" -39.698722135412979;
	setAttr ".LeftForeArmJointOrienty" -23.485520917557963;
	setAttr ".LeftForeArmJointOrientz" 122.03385742356367;
	setAttr ".LeftForeArmMinRLimitx" -45;
	setAttr ".LeftForeArmMinRLimity" -45;
	setAttr ".LeftForeArmMinRLimitz" -45;
	setAttr ".LeftForeArmMaxRLimitx" 45;
	setAttr ".LeftForeArmMaxRLimity" 45;
	setAttr ".LeftForeArmMaxRLimitz" 45;
	setAttr ".LeftHandTx" 71.709864140000064;
	setAttr ".LeftHandTy" 146.58868419999976;
	setAttr ".LeftHandTz" 2.6645352591003757e-015;
	setAttr ".LeftHandRx" -11.913326135416764;
	setAttr ".LeftHandRy" -50.329946735268649;
	setAttr ".LeftHandRz" -81.965888354672231;
	setAttr ".LeftHandSx" 1.0000000000000002;
	setAttr ".LeftHandSz" 0.99999999999999989;
	setAttr ".LeftHandJointOrientx" -100.73802301308197;
	setAttr ".LeftHandJointOrienty" -76.183997094783194;
	setAttr ".LeftHandJointOrientz" -115.61409083556042;
	setAttr ".LeftHandMinRLimitx" -45;
	setAttr ".LeftHandMinRLimity" -45;
	setAttr ".LeftHandMinRLimitz" -45;
	setAttr ".LeftHandMaxRLimitx" 45;
	setAttr ".LeftHandMaxRLimity" 45;
	setAttr ".LeftHandMaxRLimitz" 45;
	setAttr ".RightArmTx" -17.707251069999941;
	setAttr ".RightArmTy" 146.58868419999993;
	setAttr ".RightArmRx" 178.64146763734399;
	setAttr ".RightArmRy" 10.933297019161074;
	setAttr ".RightArmRz" 173.97597781886057;
	setAttr ".RightArmSz" 0.99999999999999989;
	setAttr ".RightArmJointOrientx" 178.64146763734399;
	setAttr ".RightArmJointOrienty" 10.933297019161078;
	setAttr ".RightArmJointOrientz" -155.61221849627708;
	setAttr ".RightArmMinRLimitx" -45;
	setAttr ".RightArmMinRLimity" -45;
	setAttr ".RightArmMinRLimitz" -45;
	setAttr ".RightArmMaxRLimitx" 45;
	setAttr ".RightArmMaxRLimity" 45;
	setAttr ".RightArmMaxRLimitz" 45;
	setAttr ".RightForeArmTx" -45.012716769999912;
	setAttr ".RightForeArmTy" 150.00288216303829;
	setAttr ".RightForeArmTz" -5.3157354550311;
	setAttr ".RightForeArmRx" 14.309199197227956;
	setAttr ".RightForeArmRy" 27.576677655716832;
	setAttr ".RightForeArmRz" 126.20434032489972;
	setAttr ".RightForeArmSz" 0.99999999999999978;
	setAttr ".RightForeArmJointOrientx" -156.05607077571278;
	setAttr ".RightForeArmJointOrienty" -20.916511187598104;
	setAttr ".RightForeArmJointOrientz" 43.930546533665115;
	setAttr ".RightForeArmMinRLimitx" -45;
	setAttr ".RightForeArmMinRLimity" -45;
	setAttr ".RightForeArmMinRLimitz" -45;
	setAttr ".RightForeArmMaxRLimitx" 45;
	setAttr ".RightForeArmMaxRLimity" 45;
	setAttr ".RightForeArmMaxRLimitz" 45;
	setAttr ".RightHandTx" -71.709864140000064;
	setAttr ".RightHandTy" 146.58868419999976;
	setAttr ".RightHandTz" -8.8817841970012523e-016;
	setAttr ".RightHandRx" 105.15629845739157;
	setAttr ".RightHandRy" 64.645404004952056;
	setAttr ".RightHandRz" -160.20905843505432;
	setAttr ".RightHandSx" 0.99999999999999978;
	setAttr ".RightHandJointOrientx" 43.349476774563563;
	setAttr ".RightHandJointOrienty" 55.427184345308341;
	setAttr ".RightHandJointOrientz" 22.144260474254981;
	setAttr ".RightHandMinRLimitx" -45;
	setAttr ".RightHandMinRLimity" -45;
	setAttr ".RightHandMinRLimitz" -45;
	setAttr ".RightHandMaxRLimitx" 45;
	setAttr ".RightHandMaxRLimity" 45;
	setAttr ".RightHandMaxRLimitz" 45;
	setAttr ".HeadTx" -8.8817841970012523e-015;
	setAttr ".HeadTy" 165.00000000000006;
	setAttr ".HeadRz" 124.35608894098164;
	setAttr ".HeadSx" 1.0000000000000002;
	setAttr ".HeadSy" 1.0000000000000002;
	setAttr ".HeadJointOrientz" 154.76789262584398;
	setAttr ".HeadMinRLimitx" -45;
	setAttr ".HeadMinRLimity" -45;
	setAttr ".HeadMinRLimitz" -45;
	setAttr ".HeadMaxRLimitx" 45;
	setAttr ".HeadMaxRLimity" 45;
	setAttr ".HeadMaxRLimitz" 45;
	setAttr ".LeftToeBaseTx" 8.910009227999959;
	setAttr ".LeftToeBaseTy" 1.8880791539999935;
	setAttr ".LeftToeBaseTz" 6.8367108973667534;
	setAttr ".LeftToeBaseRx" 21.82333689129695;
	setAttr ".LeftToeBaseRy" -41.064868570148342;
	setAttr ".LeftToeBaseRz" 56.730348934202283;
	setAttr ".LeftToeBaseSx" 0.99999999999999989;
	setAttr ".LeftToeBaseSy" 0.99999999999999989;
	setAttr ".LeftToeBaseSz" 0.99999999999999989;
	setAttr ".LeftToeBaseJointOrientx" 105.06036864235757;
	setAttr ".LeftToeBaseJointOrienty" -19.839074474198963;
	setAttr ".LeftToeBaseJointOrientz" 39.049558097108402;
	setAttr ".LeftToeBaseMinRLimitx" -45;
	setAttr ".LeftToeBaseMinRLimity" -45;
	setAttr ".LeftToeBaseMinRLimitz" -45;
	setAttr ".LeftToeBaseMaxRLimitx" 45;
	setAttr ".LeftToeBaseMaxRLimity" 45;
	setAttr ".LeftToeBaseMaxRLimitz" 45;
	setAttr ".RightToeBaseTx" -8.9100092279999572;
	setAttr ".RightToeBaseTy" 1.8880791539999926;
	setAttr ".RightToeBaseTz" 6.8367108973667534;
	setAttr ".RightToeBaseRx" 111.48001722481453;
	setAttr ".RightToeBaseRy" -39.556069955577442;
	setAttr ".RightToeBaseRz" 61.025798729624697;
	setAttr ".RightToeBaseSx" 1.0000000000000002;
	setAttr ".RightToeBaseSy" 1.0000000000000004;
	setAttr ".RightToeBaseSz" 1.0000000000000004;
	setAttr ".RightToeBaseJointOrientx" -69.896760531974408;
	setAttr ".RightToeBaseJointOrienty" -57.244645620553754;
	setAttr ".RightToeBaseJointOrientz" -160.84987620597857;
	setAttr ".RightToeBaseMinRLimitx" -45;
	setAttr ".RightToeBaseMinRLimity" -45;
	setAttr ".RightToeBaseMinRLimitz" -45;
	setAttr ".RightToeBaseMaxRLimitx" 45;
	setAttr ".RightToeBaseMaxRLimity" 45;
	setAttr ".RightToeBaseMaxRLimitz" 45;
	setAttr ".LeftShoulderTx" 7.0000004769999027;
	setAttr ".LeftShoulderTy" 146.58854679999999;
	setAttr ".LeftShoulderRz" -30.411803684862367;
	setAttr ".LeftShoulderJointOrientz" 113.76492079920989;
	setAttr ".LeftShoulderMinRLimitx" -45;
	setAttr ".LeftShoulderMinRLimity" -45;
	setAttr ".LeftShoulderMinRLimitz" -45;
	setAttr ".LeftShoulderMaxRLimitx" 45;
	setAttr ".LeftShoulderMaxRLimity" 45;
	setAttr ".LeftShoulderMaxRLimitz" 45;
	setAttr ".RightShoulderTx" -7.0000004769999027;
	setAttr ".RightShoulderTy" 146.58854679999999;
	setAttr ".RightShoulderRz" -30.411803684862367;
	setAttr ".RightShoulderJointOrientz" 113.76492079920989;
	setAttr ".RightShoulderMinRLimitx" -45;
	setAttr ".RightShoulderMinRLimity" -45;
	setAttr ".RightShoulderMinRLimitz" -45;
	setAttr ".RightShoulderMaxRLimitx" 45;
	setAttr ".RightShoulderMaxRLimity" 45;
	setAttr ".RightShoulderMaxRLimitz" 45;
	setAttr ".NeckTx" -1.8118839761882555e-013;
	setAttr ".NeckTy" 153.971843256429;
	setAttr ".NeckRz" -30.411803684862367;
	setAttr ".NeckJointOrientz" 113.76492079920989;
	setAttr ".NeckMinRLimitx" -45;
	setAttr ".NeckMinRLimity" -45;
	setAttr ".NeckMinRLimitz" -45;
	setAttr ".NeckMaxRLimitx" 45;
	setAttr ".NeckMaxRLimity" 45;
	setAttr ".NeckMaxRLimitz" 45;
	setAttr ".LeftFingerBaseTx" 80.519743440000028;
	setAttr ".LeftFingerBaseTy" 147.08957459999999;
	setAttr ".LeftFingerBaseTz" 1.304684401;
	setAttr ".RightFingerBaseTx" -80.519743440000028;
	setAttr ".RightFingerBaseTy" 147.08957459999999;
	setAttr ".RightFingerBaseTz" 1.304684401;
	setAttr ".Spine1Ty" 119.66666666666667;
	setAttr ".Spine2Ty" 132.33333333333334;
	setAttr ".Spine3Ty" 119;
	setAttr ".Spine4Ty" 123;
	setAttr ".Spine5Ty" 127;
	setAttr ".Spine6Ty" 131;
	setAttr ".Spine7Ty" 135;
	setAttr ".Spine8Ty" 139;
	setAttr ".Spine9Ty" 143;
	setAttr ".Neck1Tx" 2.2204460492503131e-015;
	setAttr ".Neck1Ty" 159.4859216282145;
	setAttr ".Neck2Ty" 149;
	setAttr ".Neck3Ty" 151;
	setAttr ".Neck4Ty" 153;
	setAttr ".Neck5Ty" 155;
	setAttr ".Neck6Ty" 157;
	setAttr ".Neck7Ty" 159;
	setAttr ".Neck8Ty" 161;
	setAttr ".Neck9Ty" 163;
	setAttr ".LeftUpLegRollTx" 9.2594097672262627;
	setAttr ".LeftUpLegRollTy" 71.29067706999993;
	setAttr ".LeftUpLegRollTz" 2.6813641136264241;
	setAttr ".LeftLegRollTx" 9.2594097672263;
	setAttr ".LeftLegRollTy" 28.500875473499931;
	setAttr ".LeftLegRollTz" 2.6813641136264206;
	setAttr ".RightUpLegRollTx" -9.2594097672262627;
	setAttr ".RightUpLegRollTy" 71.29067706999993;
	setAttr ".RightUpLegRollTz" 2.6813641136264241;
	setAttr ".RightLegRollTx" -9.2594097672263;
	setAttr ".RightLegRollTy" 28.500875473499931;
	setAttr ".RightLegRollTz" 2.6813641136264206;
	setAttr ".LeftArmRollTx" 31.359983919999934;
	setAttr ".LeftArmRollTy" 148.29578318151908;
	setAttr ".LeftArmRollTz" -2.6578677275155513;
	setAttr ".LeftForeArmRollTx" 58.361290454999988;
	setAttr ".LeftForeArmRollTy" 148.29578318151903;
	setAttr ".LeftForeArmRollTz" -2.6578677275155491;
	setAttr ".RightArmRollTx" -31.359983919999934;
	setAttr ".RightArmRollTy" 148.29578318151908;
	setAttr ".RightArmRollTz" -2.6578677275155513;
	setAttr ".RightForeArmRollTx" -58.361290454999988;
	setAttr ".RightForeArmRollTy" 148.29578318151903;
	setAttr ".RightForeArmRollTz" -2.6578677275155491;
	setAttr ".HipsTranslationTy" 100;
	setAttr ".LeftHandThumb1Tx" 76.05862099000008;
	setAttr ".LeftHandThumb1Ty" 145.79018169999998;
	setAttr ".LeftHandThumb1Tz" 4.2824339669999913;
	setAttr ".LeftHandThumb1Rx" 165.18731776378283;
	setAttr ".LeftHandThumb1Ry" -65.386278018908527;
	setAttr ".LeftHandThumb1Rz" 164.67370865277803;
	setAttr ".LeftHandThumb1Sx" 0.99999999999999978;
	setAttr ".LeftHandThumb1Sz" 1.0000000000000002;
	setAttr ".LeftHandThumb1JointOrientx" 86.944508452037724;
	setAttr ".LeftHandThumb1JointOrienty" -37.829338024993987;
	setAttr ".LeftHandThumb1JointOrientz" -41.191188199754983;
	setAttr ".LeftHandThumb1MinRLimitx" -45;
	setAttr ".LeftHandThumb1MinRLimity" -45;
	setAttr ".LeftHandThumb1MinRLimitz" -45;
	setAttr ".LeftHandThumb1MaxRLimitx" 45;
	setAttr ".LeftHandThumb1MaxRLimity" 45;
	setAttr ".LeftHandThumb1MaxRLimitz" 45;
	setAttr ".LeftHandThumb2Tx" 78.571210930000106;
	setAttr ".LeftHandThumb2Ty" 145.25408229999994;
	setAttr ".LeftHandThumb2Tz" 4.9898882909999704;
	setAttr ".LeftHandThumb2Rx" -145.60233834496734;
	setAttr ".LeftHandThumb2Ry" -38.616531251803735;
	setAttr ".LeftHandThumb2Rz" -61.718033778966259;
	setAttr ".LeftHandThumb2Sx" 1.0000000000000002;
	setAttr ".LeftHandThumb2Sy" 0.99999999999999967;
	setAttr ".LeftHandThumb2Sz" 0.99999999999999967;
	setAttr ".LeftHandThumb2JointOrientx" 145.68550887455535;
	setAttr ".LeftHandThumb2JointOrienty" 60.41203088647795;
	setAttr ".LeftHandThumb2JointOrientz" -46.008433357560563;
	setAttr ".LeftHandThumb2MinRLimitx" -45;
	setAttr ".LeftHandThumb2MinRLimity" -45;
	setAttr ".LeftHandThumb2MinRLimitz" -45;
	setAttr ".LeftHandThumb2MaxRLimitx" 45;
	setAttr ".LeftHandThumb2MaxRLimity" 45;
	setAttr ".LeftHandThumb2MaxRLimitz" 45;
	setAttr ".LeftHandThumb3Tx" 81.114351340000141;
	setAttr ".LeftHandThumb3Ty" 145.2540690999999;
	setAttr ".LeftHandThumb3Tz" 4.9898976329999902;
	setAttr ".LeftHandThumb3Rx" -73.086716669335857;
	setAttr ".LeftHandThumb3Ry" 65.305986959526123;
	setAttr ".LeftHandThumb3Rz" 155.6480879016685;
	setAttr ".LeftHandThumb3Sx" 1.0000000000000002;
	setAttr ".LeftHandThumb3Sy" 0.99999999999999956;
	setAttr ".LeftHandThumb3Sz" 0.99999999999999967;
	setAttr ".LeftHandThumb3JointOrientx" 115.06421486415061;
	setAttr ".LeftHandThumb3JointOrienty" -15.755241904463785;
	setAttr ".LeftHandThumb3JointOrientz" 149.17379069993603;
	setAttr ".LeftHandThumb3MinRLimitx" -45;
	setAttr ".LeftHandThumb3MinRLimity" -45;
	setAttr ".LeftHandThumb3MinRLimitz" -45;
	setAttr ".LeftHandThumb3MaxRLimitx" 45;
	setAttr ".LeftHandThumb3MaxRLimity" 45;
	setAttr ".LeftHandThumb3MaxRLimitz" 45;
	setAttr ".LeftHandThumb4Tx" 83.781097480000099;
	setAttr ".LeftHandThumb4Ty" 145.25407199999987;
	setAttr ".LeftHandThumb4Tz" 4.9898894219999672;
	setAttr ".LeftHandThumb4Rx" -132.42129737710292;
	setAttr ".LeftHandThumb4Ry" 21.921761255909278;
	setAttr ".LeftHandThumb4Rz" 160.67603925958474;
	setAttr ".LeftHandThumb4Sx" 1.0000000000000002;
	setAttr ".LeftHandThumb4Sz" 0.99999999999999956;
	setAttr ".LeftHandThumb4JointOrientx" -57.029237405579757;
	setAttr ".LeftHandThumb4JointOrienty" -16.061948057083995;
	setAttr ".LeftHandThumb4JointOrientz" -40.997781358713041;
	setAttr ".LeftHandThumb4MinRLimitx" -45;
	setAttr ".LeftHandThumb4MinRLimity" -45;
	setAttr ".LeftHandThumb4MinRLimitz" -45;
	setAttr ".LeftHandThumb4MaxRLimitx" 45;
	setAttr ".LeftHandThumb4MaxRLimity" 45;
	setAttr ".LeftHandThumb4MaxRLimitz" 45;
	setAttr ".LeftHandIndex1Tx" 80.53184085999996;
	setAttr ".LeftHandIndex1Ty" 146.78841339999991;
	setAttr ".LeftHandIndex1Tz" 3.471669415999985;
	setAttr ".LeftHandIndex1Rx" 114.16972604772239;
	setAttr ".LeftHandIndex1Ry" -10.444517585683222;
	setAttr ".LeftHandIndex1Rz" -126.19602774102324;
	setAttr ".LeftHandIndex1Sx" 1.0000000000000002;
	setAttr ".LeftHandIndex1Sy" 0.99999999999999956;
	setAttr ".LeftHandIndex1Sz" 1.0000000000000002;
	setAttr ".LeftHandIndex1JointOrientx" 87.089312165814604;
	setAttr ".LeftHandIndex1JointOrienty" 33.993759043558832;
	setAttr ".LeftHandIndex1JointOrientz" -44.694601296632996;
	setAttr ".LeftHandIndex1MinRLimitx" -45;
	setAttr ".LeftHandIndex1MinRLimity" -45;
	setAttr ".LeftHandIndex1MinRLimitz" -45;
	setAttr ".LeftHandIndex1MaxRLimitx" 45;
	setAttr ".LeftHandIndex1MaxRLimity" 45;
	setAttr ".LeftHandIndex1MaxRLimitz" 45;
	setAttr ".LeftHandIndex2Tx" 84.75459546000009;
	setAttr ".LeftHandIndex2Ty" 146.7883913;
	setAttr ".LeftHandIndex2Tz" 3.6188684349999649;
	setAttr ".LeftHandIndex2Rx" 37.782064619842224;
	setAttr ".LeftHandIndex2Ry" 77.170313586288842;
	setAttr ".LeftHandIndex2Rz" -9.7399559328856657;
	setAttr ".LeftHandIndex2Sx" 0.99999999999999967;
	setAttr ".LeftHandIndex2Sy" 1.0000000000000002;
	setAttr ".LeftHandIndex2Sz" 1.0000000000000002;
	setAttr ".LeftHandIndex2JointOrientx" -162.54020648016873;
	setAttr ".LeftHandIndex2JointOrienty" -11.764502651854691;
	setAttr ".LeftHandIndex2JointOrientz" -106.25578670343249;
	setAttr ".LeftHandIndex2MinRLimitx" -45;
	setAttr ".LeftHandIndex2MinRLimity" -45;
	setAttr ".LeftHandIndex2MinRLimitz" -45;
	setAttr ".LeftHandIndex2MaxRLimitx" 45;
	setAttr ".LeftHandIndex2MaxRLimity" 45;
	setAttr ".LeftHandIndex2MaxRLimitz" 45;
	setAttr ".LeftHandIndex3Tx" 87.406920909999982;
	setAttr ".LeftHandIndex3Ty" 146.78837750000054;
	setAttr ".LeftHandIndex3Tz" 3.71132441499998;
	setAttr ".LeftHandIndex3Rx" 80.436937384154461;
	setAttr ".LeftHandIndex3Ry" 47.19396065664931;
	setAttr ".LeftHandIndex3Rz" -49.219228490638123;
	setAttr ".LeftHandIndex3Sx" 0.99999999999999956;
	setAttr ".LeftHandIndex3Sy" 1.0000000000000002;
	setAttr ".LeftHandIndex3Sz" 1.0000000000000002;
	setAttr ".LeftHandIndex3JointOrientx" 81.599303910816744;
	setAttr ".LeftHandIndex3JointOrienty" -32.691466007164742;
	setAttr ".LeftHandIndex3JointOrientz" -8.7452861968446385;
	setAttr ".LeftHandIndex3MinRLimitx" -45;
	setAttr ".LeftHandIndex3MinRLimity" -45;
	setAttr ".LeftHandIndex3MinRLimitz" -45;
	setAttr ".LeftHandIndex3MaxRLimitx" 45;
	setAttr ".LeftHandIndex3MaxRLimity" 45;
	setAttr ".LeftHandIndex3MaxRLimitz" 45;
	setAttr ".LeftHandIndex4Tx" 89.363955140000286;
	setAttr ".LeftHandIndex4Ty" 146.78836729999998;
	setAttr ".LeftHandIndex4Tz" 3.7795433150000015;
	setAttr ".LeftHandIndex4Rx" 26.519482188075933;
	setAttr ".LeftHandIndex4Ry" 193.75945485440317;
	setAttr ".LeftHandIndex4Rz" 22.645542476847279;
	setAttr ".LeftHandIndex4Sx" 1.0000000000000002;
	setAttr ".LeftHandIndex4Sy" 1.0000000000000002;
	setAttr ".LeftHandIndex4Sz" 0.99999999999999967;
	setAttr ".LeftHandIndex4JointOrientx" -49.63265718809641;
	setAttr ".LeftHandIndex4JointOrienty" -64.187903015513285;
	setAttr ".LeftHandIndex4JointOrientz" -150.75873363182032;
	setAttr ".LeftHandIndex4MinRLimitx" -45;
	setAttr ".LeftHandIndex4MinRLimity" -45;
	setAttr ".LeftHandIndex4MinRLimitz" -45;
	setAttr ".LeftHandIndex4MaxRLimitx" 45;
	setAttr ".LeftHandIndex4MaxRLimity" 45;
	setAttr ".LeftHandIndex4MaxRLimitz" 45;
	setAttr ".LeftHandMiddle1Tx" 80.519743500000018;
	setAttr ".LeftHandMiddle1Ty" 147.0895747000001;
	setAttr ".LeftHandMiddle1Tz" 1.30468438099998;
	setAttr ".LeftHandMiddle1Rx" 114.16972604772239;
	setAttr ".LeftHandMiddle1Ry" -10.444517585683222;
	setAttr ".LeftHandMiddle1Rz" -126.19602774102324;
	setAttr ".LeftHandMiddle1Sx" 1.0000000000000002;
	setAttr ".LeftHandMiddle1Sy" 0.99999999999999956;
	setAttr ".LeftHandMiddle1Sz" 1.0000000000000002;
	setAttr ".LeftHandMiddle1JointOrientx" 87.089312165814604;
	setAttr ".LeftHandMiddle1JointOrienty" 33.993759043558832;
	setAttr ".LeftHandMiddle1JointOrientz" -44.694601296632996;
	setAttr ".LeftHandMiddle1MinRLimitx" -45;
	setAttr ".LeftHandMiddle1MinRLimity" -45;
	setAttr ".LeftHandMiddle1MinRLimitz" -45;
	setAttr ".LeftHandMiddle1MaxRLimitx" 45;
	setAttr ".LeftHandMiddle1MaxRLimity" 45;
	setAttr ".LeftHandMiddle1MaxRLimitz" 45;
	setAttr ".LeftHandMiddle2Tx" 85.382995179999938;
	setAttr ".LeftHandMiddle2Ty" 147.08957469999979;
	setAttr ".LeftHandMiddle2Tz" 1.304986835999971;
	setAttr ".LeftHandMiddle2Rx" 37.777148325649954;
	setAttr ".LeftHandMiddle2Ry" 77.168869017781006;
	setAttr ".LeftHandMiddle2Rz" -9.7449981223077309;
	setAttr ".LeftHandMiddle2Sx" 0.99999999999999978;
	setAttr ".LeftHandMiddle2Sy" 1.0000000000000002;
	setAttr ".LeftHandMiddle2Sz" 1.0000000000000002;
	setAttr ".LeftHandMiddle2JointOrientx" -162.54032067870838;
	setAttr ".LeftHandMiddle2JointOrienty" -11.762759153295242;
	setAttr ".LeftHandMiddle2JointOrientz" -106.25522656252411;
	setAttr ".LeftHandMiddle2MinRLimitx" -45;
	setAttr ".LeftHandMiddle2MinRLimity" -45;
	setAttr ".LeftHandMiddle2MinRLimitz" -45;
	setAttr ".LeftHandMiddle2MaxRLimitx" 45;
	setAttr ".LeftHandMiddle2MaxRLimity" 45;
	setAttr ".LeftHandMiddle2MaxRLimitz" 45;
	setAttr ".LeftHandMiddle3Tx" 88.148231789999855;
	setAttr ".LeftHandMiddle3Ty" 147.08957469999967;
	setAttr ".LeftHandMiddle3Tz" 1.3051586189999784;
	setAttr ".LeftHandMiddle3Rx" 80.431919361545781;
	setAttr ".LeftHandMiddle3Ry" 47.198517716698582;
	setAttr ".LeftHandMiddle3Rz" -49.228648387923201;
	setAttr ".LeftHandMiddle3Sx" 0.99999999999999956;
	setAttr ".LeftHandMiddle3Sy" 1.0000000000000002;
	setAttr ".LeftHandMiddle3Sz" 1.0000000000000002;
	setAttr ".LeftHandMiddle3JointOrientx" 81.604913696353961;
	setAttr ".LeftHandMiddle3JointOrienty" -32.684973018717038;
	setAttr ".LeftHandMiddle3JointOrientz" -8.7526011037523563;
	setAttr ".LeftHandMiddle3MinRLimitx" -45;
	setAttr ".LeftHandMiddle3MinRLimity" -45;
	setAttr ".LeftHandMiddle3MinRLimitz" -45;
	setAttr ".LeftHandMiddle3MaxRLimitx" 45;
	setAttr ".LeftHandMiddle3MaxRLimity" 45;
	setAttr ".LeftHandMiddle3MaxRLimitz" 45;
	setAttr ".LeftHandMiddle4Tx" 90.153863950000016;
	setAttr ".LeftHandMiddle4Ty" 147.08957469999973;
	setAttr ".LeftHandMiddle4Tz" 1.3052822149999972;
	setAttr ".LeftHandMiddle4Rx" 26.545832853783047;
	setAttr ".LeftHandMiddle4Ry" 193.7616894341887;
	setAttr ".LeftHandMiddle4Rz" 22.649536297139875;
	setAttr ".LeftHandMiddle4Sx" 1.0000000000000004;
	setAttr ".LeftHandMiddle4Sy" 1.0000000000000004;
	setAttr ".LeftHandMiddle4Sz" 0.99999999999999989;
	setAttr ".LeftHandMiddle4JointOrientx" -49.601387618588774;
	setAttr ".LeftHandMiddle4JointOrienty" -64.196905946648457;
	setAttr ".LeftHandMiddle4JointOrientz" -150.7580981602722;
	setAttr ".LeftHandMiddle4MinRLimitx" -45;
	setAttr ".LeftHandMiddle4MinRLimity" -45;
	setAttr ".LeftHandMiddle4MinRLimitz" -45;
	setAttr ".LeftHandMiddle4MaxRLimitx" 45;
	setAttr ".LeftHandMiddle4MaxRLimity" 45;
	setAttr ".LeftHandMiddle4MaxRLimitz" 45;
	setAttr ".LeftHandRing1Tx" 80.603623929999927;
	setAttr ".LeftHandRing1Ty" 146.96860380000007;
	setAttr ".LeftHandRing1Tz" -0.79315890900003194;
	setAttr ".LeftHandRing1Rx" 114.16972604772239;
	setAttr ".LeftHandRing1Ry" -10.444517585683222;
	setAttr ".LeftHandRing1Rz" -126.19602774102324;
	setAttr ".LeftHandRing1Sx" 1.0000000000000002;
	setAttr ".LeftHandRing1Sy" 0.99999999999999956;
	setAttr ".LeftHandRing1Sz" 1.0000000000000002;
	setAttr ".LeftHandRing1JointOrientx" 87.089312165814604;
	setAttr ".LeftHandRing1JointOrienty" 33.993759043558832;
	setAttr ".LeftHandRing1JointOrientz" -44.694601296632996;
	setAttr ".LeftHandRing1MinRLimitx" -45;
	setAttr ".LeftHandRing1MinRLimity" -45;
	setAttr ".LeftHandRing1MinRLimitz" -45;
	setAttr ".LeftHandRing1MaxRLimitx" 45;
	setAttr ".LeftHandRing1MaxRLimity" 45;
	setAttr ".LeftHandRing1MaxRLimitz" 45;
	setAttr ".LeftHandRing2Tx" 85.141382760000056;
	setAttr ".LeftHandRing2Ty" 146.96860379999987;
	setAttr ".LeftHandRing2Tz" -0.79315882000003701;
	setAttr ".LeftHandRing2Rx" 37.777148325649954;
	setAttr ".LeftHandRing2Ry" 77.168869017781006;
	setAttr ".LeftHandRing2Rz" -9.7449981223077309;
	setAttr ".LeftHandRing2Sx" 0.99999999999999978;
	setAttr ".LeftHandRing2Sy" 1.0000000000000002;
	setAttr ".LeftHandRing2Sz" 1.0000000000000002;
	setAttr ".LeftHandRing2JointOrientx" -162.54032067870838;
	setAttr ".LeftHandRing2JointOrienty" -11.762759153295242;
	setAttr ".LeftHandRing2JointOrientz" -106.25522656252411;
	setAttr ".LeftHandRing2MinRLimitx" -45;
	setAttr ".LeftHandRing2MinRLimity" -45;
	setAttr ".LeftHandRing2MinRLimitz" -45;
	setAttr ".LeftHandRing2MaxRLimitx" 45;
	setAttr ".LeftHandRing2MaxRLimity" 45;
	setAttr ".LeftHandRing2MaxRLimitz" 45;
	setAttr ".LeftHandRing3Tx" 87.445908620000026;
	setAttr ".LeftHandRing3Ty" 146.96860379999998;
	setAttr ".LeftHandRing3Tz" -0.79315893700001361;
	setAttr ".LeftHandRing3Rx" 80.431919361545781;
	setAttr ".LeftHandRing3Ry" 47.198517716698582;
	setAttr ".LeftHandRing3Rz" -49.228648387923201;
	setAttr ".LeftHandRing3Sx" 0.99999999999999956;
	setAttr ".LeftHandRing3Sy" 1.0000000000000002;
	setAttr ".LeftHandRing3Sz" 1.0000000000000002;
	setAttr ".LeftHandRing3JointOrientx" 81.604913696353961;
	setAttr ".LeftHandRing3JointOrienty" -32.684973018717038;
	setAttr ".LeftHandRing3JointOrientz" -8.7526011037523563;
	setAttr ".LeftHandRing3MinRLimitx" -45;
	setAttr ".LeftHandRing3MinRLimity" -45;
	setAttr ".LeftHandRing3MinRLimitz" -45;
	setAttr ".LeftHandRing3MaxRLimitx" 45;
	setAttr ".LeftHandRing3MaxRLimity" 45;
	setAttr ".LeftHandRing3MaxRLimitz" 45;
	setAttr ".LeftHandRing4Tx" 89.369255980000005;
	setAttr ".LeftHandRing4Ty" 146.96860379999993;
	setAttr ".LeftHandRing4Tz" -0.79315975400001681;
	setAttr ".LeftHandRing4Rx" 26.545832853783047;
	setAttr ".LeftHandRing4Ry" 193.7616894341887;
	setAttr ".LeftHandRing4Rz" 22.649536297139875;
	setAttr ".LeftHandRing4Sx" 1.0000000000000004;
	setAttr ".LeftHandRing4Sy" 1.0000000000000004;
	setAttr ".LeftHandRing4Sz" 0.99999999999999989;
	setAttr ".LeftHandRing4JointOrientx" -49.601387618588774;
	setAttr ".LeftHandRing4JointOrienty" -64.196905946648457;
	setAttr ".LeftHandRing4JointOrientz" -150.7580981602722;
	setAttr ".LeftHandRing4MinRLimitx" -45;
	setAttr ".LeftHandRing4MinRLimity" -45;
	setAttr ".LeftHandRing4MinRLimitz" -45;
	setAttr ".LeftHandRing4MaxRLimitx" 45;
	setAttr ".LeftHandRing4MaxRLimity" 45;
	setAttr ".LeftHandRing4MaxRLimitz" 45;
	setAttr ".LeftHandPinky1Tx" 80.592138830000053;
	setAttr ".LeftHandPinky1Ty" 146.27565720000021;
	setAttr ".LeftHandPinky1Tz" -2.4903564650000178;
	setAttr ".LeftHandPinky1Rx" 114.16972604772239;
	setAttr ".LeftHandPinky1Ry" -10.444517585683222;
	setAttr ".LeftHandPinky1Rz" -126.19602774102324;
	setAttr ".LeftHandPinky1Sx" 1.0000000000000002;
	setAttr ".LeftHandPinky1Sy" 0.99999999999999956;
	setAttr ".LeftHandPinky1Sz" 1.0000000000000002;
	setAttr ".LeftHandPinky1JointOrientx" 87.089312165814604;
	setAttr ".LeftHandPinky1JointOrienty" 33.993759043558832;
	setAttr ".LeftHandPinky1JointOrientz" -44.694601296632996;
	setAttr ".LeftHandPinky1MinRLimitx" -45;
	setAttr ".LeftHandPinky1MinRLimity" -45;
	setAttr ".LeftHandPinky1MinRLimitz" -45;
	setAttr ".LeftHandPinky1MaxRLimitx" 45;
	setAttr ".LeftHandPinky1MaxRLimity" 45;
	setAttr ".LeftHandPinky1MaxRLimitz" 45;
	setAttr ".LeftHandPinky2Tx" 83.636238160000147;
	setAttr ".LeftHandPinky2Ty" 146.27569780000013;
	setAttr ".LeftHandPinky2Tz" -2.4903564650000334;
	setAttr ".LeftHandPinky2Rx" 37.777148325649954;
	setAttr ".LeftHandPinky2Ry" 77.168869017781006;
	setAttr ".LeftHandPinky2Rz" -9.7449981223077309;
	setAttr ".LeftHandPinky2Sx" 0.99999999999999978;
	setAttr ".LeftHandPinky2Sy" 1.0000000000000002;
	setAttr ".LeftHandPinky2Sz" 1.0000000000000002;
	setAttr ".LeftHandPinky2JointOrientx" -162.54032067870838;
	setAttr ".LeftHandPinky2JointOrienty" -11.762759153295242;
	setAttr ".LeftHandPinky2JointOrientz" -106.25522656252411;
	setAttr ".LeftHandPinky2MinRLimitx" -45;
	setAttr ".LeftHandPinky2MinRLimity" -45;
	setAttr ".LeftHandPinky2MinRLimitz" -45;
	setAttr ".LeftHandPinky2MaxRLimitx" 45;
	setAttr ".LeftHandPinky2MaxRLimity" 45;
	setAttr ".LeftHandPinky2MaxRLimitz" 45;
	setAttr ".LeftHandPinky3Tx" 85.610739649999928;
	setAttr ".LeftHandPinky3Ty" 146.27572409999971;
	setAttr ".LeftHandPinky3Tz" -2.4903566080000372;
	setAttr ".LeftHandPinky3Rx" 80.431919361545781;
	setAttr ".LeftHandPinky3Ry" 47.198517716698582;
	setAttr ".LeftHandPinky3Rz" -49.228648387923201;
	setAttr ".LeftHandPinky3Sx" 0.99999999999999956;
	setAttr ".LeftHandPinky3Sy" 1.0000000000000002;
	setAttr ".LeftHandPinky3Sz" 1.0000000000000002;
	setAttr ".LeftHandPinky3JointOrientx" 81.604913696353961;
	setAttr ".LeftHandPinky3JointOrienty" -32.684973018717038;
	setAttr ".LeftHandPinky3JointOrientz" -8.7526011037523563;
	setAttr ".LeftHandPinky3MinRLimitx" -45;
	setAttr ".LeftHandPinky3MinRLimity" -45;
	setAttr ".LeftHandPinky3MinRLimitz" -45;
	setAttr ".LeftHandPinky3MaxRLimitx" 45;
	setAttr ".LeftHandPinky3MaxRLimity" 45;
	setAttr ".LeftHandPinky3MaxRLimitz" 45;
	setAttr ".LeftHandPinky4Tx" 87.277354300000113;
	setAttr ".LeftHandPinky4Ty" 146.27574629999995;
	setAttr ".LeftHandPinky4Tz" -2.4903558169999975;
	setAttr ".LeftHandPinky4Rx" 26.545832853783047;
	setAttr ".LeftHandPinky4Ry" 193.7616894341887;
	setAttr ".LeftHandPinky4Rz" 22.649536297139875;
	setAttr ".LeftHandPinky4Sx" 1.0000000000000004;
	setAttr ".LeftHandPinky4Sy" 1.0000000000000004;
	setAttr ".LeftHandPinky4Sz" 0.99999999999999989;
	setAttr ".LeftHandPinky4JointOrientx" -49.601387618588774;
	setAttr ".LeftHandPinky4JointOrienty" -64.196905946648457;
	setAttr ".LeftHandPinky4JointOrientz" -150.7580981602722;
	setAttr ".LeftHandPinky4MinRLimitx" -45;
	setAttr ".LeftHandPinky4MinRLimity" -45;
	setAttr ".LeftHandPinky4MinRLimitz" -45;
	setAttr ".LeftHandPinky4MaxRLimitx" 45;
	setAttr ".LeftHandPinky4MaxRLimity" 45;
	setAttr ".LeftHandPinky4MaxRLimitz" 45;
	setAttr ".LeftHandExtraFinger1Tx" 80.592138829999996;
	setAttr ".LeftHandExtraFinger1Ty" 146.7884134;
	setAttr ".LeftHandExtraFinger1Tz" -4.4903564649999996;
	setAttr ".LeftHandExtraFinger1Ry" -0.03490658477808721;
	setAttr ".LeftHandExtraFinger1Rz" -5.2244860362123464e-006;
	setAttr ".LeftHandExtraFinger2Tx" 82.636238160000005;
	setAttr ".LeftHandExtraFinger2Ty" 146.7883913;
	setAttr ".LeftHandExtraFinger2Tz" -4.4903564649999996;
	setAttr ".LeftHandExtraFinger2Ry" -0.03490658477808721;
	setAttr ".LeftHandExtraFinger2Rz" -5.2244860362123464e-006;
	setAttr ".LeftHandExtraFinger3Tx" 84.610739649999999;
	setAttr ".LeftHandExtraFinger3Ty" 146.7883775;
	setAttr ".LeftHandExtraFinger3Tz" -4.4903566079999999;
	setAttr ".LeftHandExtraFinger3Ry" -0.03490658477808721;
	setAttr ".LeftHandExtraFinger3Rz" -5.2244860362123464e-006;
	setAttr ".LeftHandExtraFinger4Tx" 86.277354299999999;
	setAttr ".LeftHandExtraFinger4Ty" 146.7883673;
	setAttr ".LeftHandExtraFinger4Tz" -4.4903558170000002;
	setAttr ".LeftHandExtraFinger4Ry" -0.03490658477808721;
	setAttr ".LeftHandExtraFinger4Rz" -5.2244860362123464e-006;
	setAttr ".RightHandThumb1Tx" -76.058620990000094;
	setAttr ".RightHandThumb1Ty" 145.79018170000001;
	setAttr ".RightHandThumb1Tz" 4.2824339669999949;
	setAttr ".RightHandThumb1Rx" 84.31098077836883;
	setAttr ".RightHandThumb1Ry" 0.52466115974710348;
	setAttr ".RightHandThumb1Rz" -136.65044156451137;
	setAttr ".RightHandThumb1Sy" 0.99999999999999967;
	setAttr ".RightHandThumb1JointOrientx" -14.143215185739152;
	setAttr ".RightHandThumb1JointOrienty" 36.963772863592794;
	setAttr ".RightHandThumb1JointOrientz" 59.894099048129888;
	setAttr ".RightHandThumb1MinRLimitx" -45;
	setAttr ".RightHandThumb1MinRLimity" -45;
	setAttr ".RightHandThumb1MinRLimitz" -45;
	setAttr ".RightHandThumb1MaxRLimitx" 45;
	setAttr ".RightHandThumb1MaxRLimity" 45;
	setAttr ".RightHandThumb1MaxRLimitz" 45;
	setAttr ".RightHandThumb2Tx" -78.571210930000134;
	setAttr ".RightHandThumb2Ty" 145.25408229999996;
	setAttr ".RightHandThumb2Tz" 4.9898882909999767;
	setAttr ".RightHandThumb2Rx" -108.45073002541356;
	setAttr ".RightHandThumb2Ry" -41.918353660863801;
	setAttr ".RightHandThumb2Rz" -102.92598007070323;
	setAttr ".RightHandThumb2Sx" 0.99999999999999989;
	setAttr ".RightHandThumb2JointOrientx" -170.34197255632242;
	setAttr ".RightHandThumb2JointOrienty" 20.139292411158664;
	setAttr ".RightHandThumb2JointOrientz" 49.259154553438862;
	setAttr ".RightHandThumb2MinRLimitx" -45;
	setAttr ".RightHandThumb2MinRLimity" -45;
	setAttr ".RightHandThumb2MinRLimitz" -45;
	setAttr ".RightHandThumb2MaxRLimitx" 45;
	setAttr ".RightHandThumb2MaxRLimity" 45;
	setAttr ".RightHandThumb2MaxRLimitz" 45;
	setAttr ".RightHandThumb3Tx" -81.114351340000113;
	setAttr ".RightHandThumb3Ty" 145.2540690999999;
	setAttr ".RightHandThumb3Tz" 4.9898976329999822;
	setAttr ".RightHandThumb3Rx" 102.71948149192295;
	setAttr ".RightHandThumb3Ry" -7.8074535126274514;
	setAttr ".RightHandThumb3Rz" 132.62627740673872;
	setAttr ".RightHandThumb3Sz" 1.0000000000000002;
	setAttr ".RightHandThumb3JointOrientx" -4.2896279448032084;
	setAttr ".RightHandThumb3JointOrienty" 67.74147836349735;
	setAttr ".RightHandThumb3JointOrientz" -149.46226431642106;
	setAttr ".RightHandThumb3MinRLimitx" -45;
	setAttr ".RightHandThumb3MinRLimity" -45;
	setAttr ".RightHandThumb3MinRLimitz" -45;
	setAttr ".RightHandThumb3MaxRLimitx" 45;
	setAttr ".RightHandThumb3MaxRLimity" 45;
	setAttr ".RightHandThumb3MaxRLimitz" 45;
	setAttr ".RightHandThumb4Tx" -83.781097480000085;
	setAttr ".RightHandThumb4Ty" 145.25407199999989;
	setAttr ".RightHandThumb4Tz" 4.9898894219999779;
	setAttr ".RightHandThumb4Rx" -1.8646899304325975;
	setAttr ".RightHandThumb4Ry" 47.154844856800736;
	setAttr ".RightHandThumb4Rz" 163.54227241842491;
	setAttr ".RightHandThumb4Sy" 1.0000000000000002;
	setAttr ".RightHandThumb4Sz" 1.0000000000000002;
	setAttr ".RightHandThumb4JointOrientx" -122.11324446811993;
	setAttr ".RightHandThumb4JointOrienty" 9.4055033807564623;
	setAttr ".RightHandThumb4JointOrientz" -60.993176780563005;
	setAttr ".RightHandThumb4MinRLimitx" -45;
	setAttr ".RightHandThumb4MinRLimity" -45;
	setAttr ".RightHandThumb4MinRLimitz" -45;
	setAttr ".RightHandThumb4MaxRLimitx" 45;
	setAttr ".RightHandThumb4MaxRLimity" 45;
	setAttr ".RightHandThumb4MaxRLimitz" 45;
	setAttr ".RightHandIndex1Tx" -80.531840859999974;
	setAttr ".RightHandIndex1Ty" 146.78841339999991;
	setAttr ".RightHandIndex1Tz" 3.4716694159999735;
	setAttr ".RightHandIndex1Rx" 71.744703085648069;
	setAttr ".RightHandIndex1Ry" 71.554267559850445;
	setAttr ".RightHandIndex1Rz" -153.97359527528323;
	setAttr ".RightHandIndex1Sx" 0.99999999999999978;
	setAttr ".RightHandIndex1Sy" 1.0000000000000002;
	setAttr ".RightHandIndex1Sz" 1.0000000000000002;
	setAttr ".RightHandIndex1JointOrientx" -39.213046177044284;
	setAttr ".RightHandIndex1JointOrienty" 0.073247472877887659;
	setAttr ".RightHandIndex1JointOrientz" -7.2803420073408835;
	setAttr ".RightHandIndex1MinRLimitx" -45;
	setAttr ".RightHandIndex1MinRLimity" -45;
	setAttr ".RightHandIndex1MinRLimitz" -45;
	setAttr ".RightHandIndex1MaxRLimitx" 45;
	setAttr ".RightHandIndex1MaxRLimity" 45;
	setAttr ".RightHandIndex1MaxRLimitz" 45;
	setAttr ".RightHandIndex2Tx" -84.754595460000061;
	setAttr ".RightHandIndex2Ty" 146.78839129999997;
	setAttr ".RightHandIndex2Tz" 3.6188684349999765;
	setAttr ".RightHandIndex2Rx" -6.5455022836711754;
	setAttr ".RightHandIndex2Ry" 49.020798617557283;
	setAttr ".RightHandIndex2Rz" -62.483236854688251;
	setAttr ".RightHandIndex2Sx" 0.99999999999999989;
	setAttr ".RightHandIndex2Sy" 1.0000000000000002;
	setAttr ".RightHandIndex2JointOrientx" -164.04599316587462;
	setAttr ".RightHandIndex2JointOrienty" 44.624997928192926;
	setAttr ".RightHandIndex2JointOrientz" -2.9684558651065718;
	setAttr ".RightHandIndex2MinRLimitx" -45;
	setAttr ".RightHandIndex2MinRLimity" -45;
	setAttr ".RightHandIndex2MinRLimitz" -45;
	setAttr ".RightHandIndex2MaxRLimitx" 45;
	setAttr ".RightHandIndex2MaxRLimity" 45;
	setAttr ".RightHandIndex2MaxRLimitz" 45;
	setAttr ".RightHandIndex3Tx" -87.406920909999968;
	setAttr ".RightHandIndex3Ty" 146.78837750000054;
	setAttr ".RightHandIndex3Tz" 3.7113244149999915;
	setAttr ".RightHandIndex3Rx" 139.41622919098089;
	setAttr ".RightHandIndex3Ry" 28.695007215652911;
	setAttr ".RightHandIndex3Rz" 73.135261872716157;
	setAttr ".RightHandIndex3Sx" 1.0000000000000002;
	setAttr ".RightHandIndex3Sy" 0.99999999999999989;
	setAttr ".RightHandIndex3Sz" 0.99999999999999989;
	setAttr ".RightHandIndex3JointOrientx" 79.592390610011748;
	setAttr ".RightHandIndex3JointOrienty" 45.487142713995723;
	setAttr ".RightHandIndex3JointOrientz" 93.978534364862938;
	setAttr ".RightHandIndex3MinRLimitx" -45;
	setAttr ".RightHandIndex3MinRLimity" -45;
	setAttr ".RightHandIndex3MinRLimitz" -45;
	setAttr ".RightHandIndex3MaxRLimitx" 45;
	setAttr ".RightHandIndex3MaxRLimity" 45;
	setAttr ".RightHandIndex3MaxRLimitz" 45;
	setAttr ".RightHandIndex4Tx" -89.363955140000272;
	setAttr ".RightHandIndex4Ty" 146.7883673;
	setAttr ".RightHandIndex4Tz" 3.7795433149999904;
	setAttr ".RightHandIndex4Rx" -167.29386693075691;
	setAttr ".RightHandIndex4Ry" 39.943508826022992;
	setAttr ".RightHandIndex4Rz" -44.091640312408735;
	setAttr ".RightHandIndex4Sx" 0.99999999999999989;
	setAttr ".RightHandIndex4Sy" 1.0000000000000002;
	setAttr ".RightHandIndex4JointOrientx" 52.241836570279155;
	setAttr ".RightHandIndex4JointOrienty" -87.604457142391439;
	setAttr ".RightHandIndex4JointOrientz" 89.2032851282639;
	setAttr ".RightHandIndex4MinRLimitx" -45;
	setAttr ".RightHandIndex4MinRLimity" -45;
	setAttr ".RightHandIndex4MinRLimitz" -45;
	setAttr ".RightHandIndex4MaxRLimitx" 45;
	setAttr ".RightHandIndex4MaxRLimity" 45;
	setAttr ".RightHandIndex4MaxRLimitz" 45;
	setAttr ".RightHandMiddle1Tx" -80.519743500000018;
	setAttr ".RightHandMiddle1Ty" 147.0895747000001;
	setAttr ".RightHandMiddle1Tz" 1.3046843809999753;
	setAttr ".RightHandMiddle1Rx" 71.744703085648069;
	setAttr ".RightHandMiddle1Ry" 71.554267559850445;
	setAttr ".RightHandMiddle1Rz" -153.97359527528323;
	setAttr ".RightHandMiddle1Sx" 0.99999999999999978;
	setAttr ".RightHandMiddle1Sy" 1.0000000000000002;
	setAttr ".RightHandMiddle1Sz" 1.0000000000000002;
	setAttr ".RightHandMiddle1JointOrientx" -39.213046177044284;
	setAttr ".RightHandMiddle1JointOrienty" 0.073247472877887659;
	setAttr ".RightHandMiddle1JointOrientz" -7.2803420073408835;
	setAttr ".RightHandMiddle1MinRLimitx" -45;
	setAttr ".RightHandMiddle1MinRLimity" -45;
	setAttr ".RightHandMiddle1MinRLimitz" -45;
	setAttr ".RightHandMiddle1MaxRLimitx" 45;
	setAttr ".RightHandMiddle1MaxRLimity" 45;
	setAttr ".RightHandMiddle1MaxRLimitz" 45;
	setAttr ".RightHandMiddle2Tx" -85.38299517999998;
	setAttr ".RightHandMiddle2Ty" 147.08957469999982;
	setAttr ".RightHandMiddle2Tz" 1.3049868359999857;
	setAttr ".RightHandMiddle2Rx" -6.5455022836711754;
	setAttr ".RightHandMiddle2Ry" 49.020798617557283;
	setAttr ".RightHandMiddle2Rz" -62.483236854688251;
	setAttr ".RightHandMiddle2Sx" 0.99999999999999989;
	setAttr ".RightHandMiddle2Sy" 1.0000000000000002;
	setAttr ".RightHandMiddle2JointOrientx" -164.04599316587462;
	setAttr ".RightHandMiddle2JointOrienty" 44.624997928192926;
	setAttr ".RightHandMiddle2JointOrientz" -2.9684558651065718;
	setAttr ".RightHandMiddle2MinRLimitx" -45;
	setAttr ".RightHandMiddle2MinRLimity" -45;
	setAttr ".RightHandMiddle2MinRLimitz" -45;
	setAttr ".RightHandMiddle2MaxRLimitx" 45;
	setAttr ".RightHandMiddle2MaxRLimity" 45;
	setAttr ".RightHandMiddle2MaxRLimitz" 45;
	setAttr ".RightHandMiddle3Tx" -88.148231789999869;
	setAttr ".RightHandMiddle3Ty" 147.0895746999997;
	setAttr ".RightHandMiddle3Tz" 1.3051586189999835;
	setAttr ".RightHandMiddle3Rx" 139.41622919098089;
	setAttr ".RightHandMiddle3Ry" 28.695007215652911;
	setAttr ".RightHandMiddle3Rz" 73.135261872716157;
	setAttr ".RightHandMiddle3Sx" 1.0000000000000002;
	setAttr ".RightHandMiddle3Sy" 0.99999999999999989;
	setAttr ".RightHandMiddle3Sz" 0.99999999999999989;
	setAttr ".RightHandMiddle3JointOrientx" 79.592390610011748;
	setAttr ".RightHandMiddle3JointOrienty" 45.487142713995723;
	setAttr ".RightHandMiddle3JointOrientz" 93.978534364862938;
	setAttr ".RightHandMiddle3MinRLimitx" -45;
	setAttr ".RightHandMiddle3MinRLimity" -45;
	setAttr ".RightHandMiddle3MinRLimitz" -45;
	setAttr ".RightHandMiddle3MaxRLimitx" 45;
	setAttr ".RightHandMiddle3MaxRLimity" 45;
	setAttr ".RightHandMiddle3MaxRLimitz" 45;
	setAttr ".RightHandMiddle4Tx" -90.153863950000002;
	setAttr ".RightHandMiddle4Ty" 147.08957469999982;
	setAttr ".RightHandMiddle4Tz" 1.3052822150000027;
	setAttr ".RightHandMiddle4Rx" -167.29386693075691;
	setAttr ".RightHandMiddle4Ry" 39.943508826022992;
	setAttr ".RightHandMiddle4Rz" -44.091640312408735;
	setAttr ".RightHandMiddle4Sx" 0.99999999999999989;
	setAttr ".RightHandMiddle4Sy" 1.0000000000000002;
	setAttr ".RightHandMiddle4JointOrientx" 52.241836570279155;
	setAttr ".RightHandMiddle4JointOrienty" -87.604457142391439;
	setAttr ".RightHandMiddle4JointOrientz" 89.2032851282639;
	setAttr ".RightHandMiddle4MinRLimitx" -45;
	setAttr ".RightHandMiddle4MinRLimity" -45;
	setAttr ".RightHandMiddle4MinRLimitz" -45;
	setAttr ".RightHandMiddle4MaxRLimitx" 45;
	setAttr ".RightHandMiddle4MaxRLimity" 45;
	setAttr ".RightHandMiddle4MaxRLimitz" 45;
	setAttr ".RightHandRing1Tx" -80.603623929999927;
	setAttr ".RightHandRing1Ty" 146.9686038000001;
	setAttr ".RightHandRing1Tz" -0.79315890900002328;
	setAttr ".RightHandRing1Rx" 71.744703085648069;
	setAttr ".RightHandRing1Ry" 71.554267559850445;
	setAttr ".RightHandRing1Rz" -153.97359527528323;
	setAttr ".RightHandRing1Sx" 0.99999999999999978;
	setAttr ".RightHandRing1Sy" 1.0000000000000002;
	setAttr ".RightHandRing1Sz" 1.0000000000000002;
	setAttr ".RightHandRing1JointOrientx" -39.213046177044284;
	setAttr ".RightHandRing1JointOrienty" 0.073247472877887659;
	setAttr ".RightHandRing1JointOrientz" -7.2803420073408835;
	setAttr ".RightHandRing1MinRLimitx" -45;
	setAttr ".RightHandRing1MinRLimity" -45;
	setAttr ".RightHandRing1MinRLimitz" -45;
	setAttr ".RightHandRing1MaxRLimitx" 45;
	setAttr ".RightHandRing1MaxRLimity" 45;
	setAttr ".RightHandRing1MaxRLimitz" 45;
	setAttr ".RightHandRing2Tx" -85.141382760000056;
	setAttr ".RightHandRing2Ty" 146.96860379999987;
	setAttr ".RightHandRing2Tz" -0.7931588200000248;
	setAttr ".RightHandRing2Rx" -6.5455022836711754;
	setAttr ".RightHandRing2Ry" 49.020798617557283;
	setAttr ".RightHandRing2Rz" -62.483236854688251;
	setAttr ".RightHandRing2Sx" 0.99999999999999989;
	setAttr ".RightHandRing2Sy" 1.0000000000000002;
	setAttr ".RightHandRing2JointOrientx" -164.04599316587462;
	setAttr ".RightHandRing2JointOrienty" 44.624997928192926;
	setAttr ".RightHandRing2JointOrientz" -2.9684558651065718;
	setAttr ".RightHandRing2MinRLimitx" -45;
	setAttr ".RightHandRing2MinRLimity" -45;
	setAttr ".RightHandRing2MinRLimitz" -45;
	setAttr ".RightHandRing2MaxRLimitx" 45;
	setAttr ".RightHandRing2MaxRLimity" 45;
	setAttr ".RightHandRing2MaxRLimitz" 45;
	setAttr ".RightHandRing3Tx" -87.445908619999983;
	setAttr ".RightHandRing3Ty" 146.96860379999998;
	setAttr ".RightHandRing3Tz" -0.79315893699999396;
	setAttr ".RightHandRing3Rx" 139.41622919098089;
	setAttr ".RightHandRing3Ry" 28.695007215652911;
	setAttr ".RightHandRing3Rz" 73.135261872716157;
	setAttr ".RightHandRing3Sx" 1.0000000000000002;
	setAttr ".RightHandRing3Sy" 0.99999999999999989;
	setAttr ".RightHandRing3Sz" 0.99999999999999989;
	setAttr ".RightHandRing3JointOrientx" 79.592390610011748;
	setAttr ".RightHandRing3JointOrienty" 45.487142713995723;
	setAttr ".RightHandRing3JointOrientz" 93.978534364862938;
	setAttr ".RightHandRing3MinRLimitx" -45;
	setAttr ".RightHandRing3MinRLimity" -45;
	setAttr ".RightHandRing3MinRLimitz" -45;
	setAttr ".RightHandRing3MaxRLimitx" 45;
	setAttr ".RightHandRing3MaxRLimity" 45;
	setAttr ".RightHandRing3MaxRLimitz" 45;
	setAttr ".RightHandRing4Tx" -89.369255979999991;
	setAttr ".RightHandRing4Ty" 146.96860379999993;
	setAttr ".RightHandRing4Tz" -0.79315975400002769;
	setAttr ".RightHandRing4Rx" -167.29386693075691;
	setAttr ".RightHandRing4Ry" 39.943508826022992;
	setAttr ".RightHandRing4Rz" -44.091640312408735;
	setAttr ".RightHandRing4Sx" 0.99999999999999989;
	setAttr ".RightHandRing4Sy" 1.0000000000000002;
	setAttr ".RightHandRing4JointOrientx" 52.241836570279155;
	setAttr ".RightHandRing4JointOrienty" -87.604457142391439;
	setAttr ".RightHandRing4JointOrientz" 89.2032851282639;
	setAttr ".RightHandRing4MinRLimitx" -45;
	setAttr ".RightHandRing4MinRLimity" -45;
	setAttr ".RightHandRing4MinRLimitz" -45;
	setAttr ".RightHandRing4MaxRLimitx" 45;
	setAttr ".RightHandRing4MaxRLimity" 45;
	setAttr ".RightHandRing4MaxRLimitz" 45;
	setAttr ".RightHandPinky1Tx" -80.592138830000039;
	setAttr ".RightHandPinky1Ty" 146.27565720000021;
	setAttr ".RightHandPinky1Tz" -2.4903564650000147;
	setAttr ".RightHandPinky1Rx" 71.744703085648069;
	setAttr ".RightHandPinky1Ry" 71.554267559850445;
	setAttr ".RightHandPinky1Rz" -153.97359527528323;
	setAttr ".RightHandPinky1Sx" 0.99999999999999978;
	setAttr ".RightHandPinky1Sy" 1.0000000000000002;
	setAttr ".RightHandPinky1Sz" 1.0000000000000002;
	setAttr ".RightHandPinky1JointOrientx" -39.213046177044284;
	setAttr ".RightHandPinky1JointOrienty" 0.073247472877887659;
	setAttr ".RightHandPinky1JointOrientz" -7.2803420073408835;
	setAttr ".RightHandPinky1MinRLimitx" -45;
	setAttr ".RightHandPinky1MinRLimity" -45;
	setAttr ".RightHandPinky1MinRLimitz" -45;
	setAttr ".RightHandPinky1MaxRLimitx" 45;
	setAttr ".RightHandPinky1MaxRLimity" 45;
	setAttr ".RightHandPinky1MaxRLimitz" 45;
	setAttr ".RightHandPinky2Tx" -83.63623816000019;
	setAttr ".RightHandPinky2Ty" 146.27569780000016;
	setAttr ".RightHandPinky2Tz" -2.4903564650000201;
	setAttr ".RightHandPinky2Rx" -6.5455022836711754;
	setAttr ".RightHandPinky2Ry" 49.020798617557283;
	setAttr ".RightHandPinky2Rz" -62.483236854688251;
	setAttr ".RightHandPinky2Sx" 0.99999999999999989;
	setAttr ".RightHandPinky2Sy" 1.0000000000000002;
	setAttr ".RightHandPinky2JointOrientx" -164.04599316587462;
	setAttr ".RightHandPinky2JointOrienty" 44.624997928192926;
	setAttr ".RightHandPinky2JointOrientz" -2.9684558651065718;
	setAttr ".RightHandPinky2MinRLimitx" -45;
	setAttr ".RightHandPinky2MinRLimity" -45;
	setAttr ".RightHandPinky2MinRLimitz" -45;
	setAttr ".RightHandPinky2MaxRLimitx" 45;
	setAttr ".RightHandPinky2MaxRLimity" 45;
	setAttr ".RightHandPinky2MaxRLimitz" 45;
	setAttr ".RightHandPinky3Tx" -85.610739649999928;
	setAttr ".RightHandPinky3Ty" 146.27572409999974;
	setAttr ".RightHandPinky3Tz" -2.4903566080000106;
	setAttr ".RightHandPinky3Rx" 139.41622919098089;
	setAttr ".RightHandPinky3Ry" 28.695007215652911;
	setAttr ".RightHandPinky3Rz" 73.135261872716157;
	setAttr ".RightHandPinky3Sx" 1.0000000000000002;
	setAttr ".RightHandPinky3Sy" 0.99999999999999989;
	setAttr ".RightHandPinky3Sz" 0.99999999999999989;
	setAttr ".RightHandPinky3JointOrientx" 79.592390610011748;
	setAttr ".RightHandPinky3JointOrienty" 45.487142713995723;
	setAttr ".RightHandPinky3JointOrientz" 93.978534364862938;
	setAttr ".RightHandPinky3MinRLimitx" -45;
	setAttr ".RightHandPinky3MinRLimity" -45;
	setAttr ".RightHandPinky3MinRLimitz" -45;
	setAttr ".RightHandPinky3MaxRLimitx" 45;
	setAttr ".RightHandPinky3MaxRLimity" 45;
	setAttr ".RightHandPinky3MaxRLimitz" 45;
	setAttr ".RightHandPinky4Tx" -87.277354300000098;
	setAttr ".RightHandPinky4Ty" 146.27574630000001;
	setAttr ".RightHandPinky4Tz" -2.4903558170000095;
	setAttr ".RightHandPinky4Rx" -167.29386693075691;
	setAttr ".RightHandPinky4Ry" 39.943508826022992;
	setAttr ".RightHandPinky4Rz" -44.091640312408735;
	setAttr ".RightHandPinky4Sx" 0.99999999999999989;
	setAttr ".RightHandPinky4Sy" 1.0000000000000002;
	setAttr ".RightHandPinky4JointOrientx" 52.241836570279155;
	setAttr ".RightHandPinky4JointOrienty" -87.604457142391439;
	setAttr ".RightHandPinky4JointOrientz" 89.2032851282639;
	setAttr ".RightHandPinky4MinRLimitx" -45;
	setAttr ".RightHandPinky4MinRLimity" -45;
	setAttr ".RightHandPinky4MinRLimitz" -45;
	setAttr ".RightHandPinky4MaxRLimitx" 45;
	setAttr ".RightHandPinky4MaxRLimity" 45;
	setAttr ".RightHandPinky4MaxRLimitz" 45;
	setAttr ".RightHandExtraFinger1Tx" -80.592138829999996;
	setAttr ".RightHandExtraFinger1Ty" 146.7884134;
	setAttr ".RightHandExtraFinger1Tz" -4.4903564649999996;
	setAttr ".RightHandExtraFinger1Ry" -0.034907713534874346;
	setAttr ".RightHandExtraFinger2Tx" -82.636238160000005;
	setAttr ".RightHandExtraFinger2Ty" 146.7883913;
	setAttr ".RightHandExtraFinger2Tz" -4.4903564649999996;
	setAttr ".RightHandExtraFinger2Ry" -0.034907713150901909;
	setAttr ".RightHandExtraFinger3Tx" -84.610739649999999;
	setAttr ".RightHandExtraFinger3Ty" 146.7883775;
	setAttr ".RightHandExtraFinger3Tz" -4.4903566079999999;
	setAttr ".RightHandExtraFinger3Ry" -0.034907713150901909;
	setAttr ".RightHandExtraFinger4Tx" -86.277354299999999;
	setAttr ".RightHandExtraFinger4Ty" 146.7883673;
	setAttr ".RightHandExtraFinger4Tz" -4.4903558170000002;
	setAttr ".RightHandExtraFinger4Ry" -0.034907713150901909;
	setAttr ".LeftFootThumb1Tx" 6.18422217;
	setAttr ".LeftFootThumb1Ty" 4.9992492679999998;
	setAttr ".LeftFootThumb1Tz" 1.930123209;
	setAttr ".LeftFootThumb2Tx" 4.551409713;
	setAttr ".LeftFootThumb2Ty" 2.6643834059999998;
	setAttr ".LeftFootThumb2Tz" 3.591937658;
	setAttr ".LeftFootThumb3Tx" 3.4619466889999999;
	setAttr ".LeftFootThumb3Ty" 1.8880788850000001;
	setAttr ".LeftFootThumb3Tz" 6.4001420700000002;
	setAttr ".LeftFootThumb4Tx" 3.4619466999999999;
	setAttr ".LeftFootThumb4Ty" 1.8880788550000001;
	setAttr ".LeftFootThumb4Tz" 9.6971958839999992;
	setAttr ".LeftFootIndex1Tx" 7.1105199679999966;
	setAttr ".LeftFootIndex1Ty" 1.8880791170000002;
	setAttr ".LeftFootIndex1Tz" 12.954720899999998;
	setAttr ".LeftFootIndex2Tx" 7.1105199749999999;
	setAttr ".LeftFootIndex2Ty" 1.8880790999999983;
	setAttr ".LeftFootIndex2Tz" 14.829727449999996;
	setAttr ".LeftFootIndex3Tx" 7.1105199809999995;
	setAttr ".LeftFootIndex3Ty" 1.888079083;
	setAttr ".LeftFootIndex3Tz" 16.763144419999996;
	setAttr ".LeftFootIndex4Tx" 7.1105199879999992;
	setAttr ".LeftFootIndex4Ty" 1.8880790649999999;
	setAttr ".LeftFootIndex4Tz" 18.850666449999999;
	setAttr ".LeftFootMiddle1Tx" 8.9167242489998646;
	setAttr ".LeftFootMiddle1Ty" 1.8880791629999889;
	setAttr ".LeftFootMiddle1Tz" 11.125471607836856;
	setAttr ".LeftFootMiddle1Rx" -50.130056878192462;
	setAttr ".LeftFootMiddle1Ry" 65.895181173668789;
	setAttr ".LeftFootMiddle1Rz" 117.24854590508791;
	setAttr ".LeftFootMiddle1Sx" 0.99999999999999989;
	setAttr ".LeftFootMiddle1Sy" 0.99999999999999967;
	setAttr ".LeftFootMiddle1Sz" 0.99999999999999989;
	setAttr ".LeftFootMiddle1JointOrientx" 79.043982325131367;
	setAttr ".LeftFootMiddle1JointOrienty" 63.333985769094063;
	setAttr ".LeftFootMiddle1JointOrientz" 176.79167183659945;
	setAttr ".LeftFootMiddle1MinRLimitx" -45;
	setAttr ".LeftFootMiddle1MinRLimity" -45;
	setAttr ".LeftFootMiddle1MinRLimitz" -45;
	setAttr ".LeftFootMiddle1MaxRLimitx" 45;
	setAttr ".LeftFootMiddle1MaxRLimity" 45;
	setAttr ".LeftFootMiddle1MaxRLimitz" 45;
	setAttr ".LeftFootMiddle2Tx" 8.9167242549997976;
	setAttr ".LeftFootMiddle2Ty" 1.888079153170886;
	setAttr ".LeftFootMiddle2Tz" 16.03588330607742;
	setAttr ".LeftFootMiddle2Rx" -163.59660439234617;
	setAttr ".LeftFootMiddle2Ry" -2.8150785147258151;
	setAttr ".LeftFootMiddle2Rz" 17.342925462353382;
	setAttr ".LeftFootMiddle2Sy" 0.99999999999999944;
	setAttr ".LeftFootMiddle2Sz" 0.99999999999999989;
	setAttr ".LeftFootMiddle2JointOrientx" -107.93378105452776;
	setAttr ".LeftFootMiddle2JointOrienty" 57.440018710498983;
	setAttr ".LeftFootMiddle2JointOrientz" -102.33842274208088;
	setAttr ".LeftFootMiddle2MinRLimitx" -45;
	setAttr ".LeftFootMiddle2MinRLimity" -45;
	setAttr ".LeftFootMiddle2MinRLimitz" -45;
	setAttr ".LeftFootMiddle2MaxRLimitx" 45;
	setAttr ".LeftFootMiddle2MaxRLimity" 45;
	setAttr ".LeftFootMiddle2MaxRLimitz" 45;
	setAttr ".LeftFootMiddle3Tx" 8.9167242610000006;
	setAttr ".LeftFootMiddle3Ty" 1.888079131;
	setAttr ".LeftFootMiddle3Tz" 16.64971237;
	setAttr ".LeftFootMiddle4Tx" 8.9167242669999993;
	setAttr ".LeftFootMiddle4Ty" 1.8880791139999999;
	setAttr ".LeftFootMiddle4Tz" 18.565581959999999;
	setAttr ".LeftFootRing1Tx" 10.723903740000003;
	setAttr ".LeftFootRing1Ty" 1.8880792109999991;
	setAttr ".LeftFootRing1Tz" 12.9547209;
	setAttr ".LeftFootRing2Tx" 10.723903740000003;
	setAttr ".LeftFootRing2Ty" 1.888079195;
	setAttr ".LeftFootRing2Tz" 14.713452259999999;
	setAttr ".LeftFootRing3Tx" 10.723903750000002;
	setAttr ".LeftFootRing3Ty" 1.8880791800000001;
	setAttr ".LeftFootRing3Tz" 16.472174209999999;
	setAttr ".LeftFootRing4Tx" 10.723903760000002;
	setAttr ".LeftFootRing4Ty" 1.8880791640000001;
	setAttr ".LeftFootRing4Tz" 18.27484922;
	setAttr ".LeftFootPinky1Tx" 12.52979668;
	setAttr ".LeftFootPinky1Ty" 1.888079257;
	setAttr ".LeftFootPinky1Tz" 12.9547209;
	setAttr ".LeftFootPinky2Tx" 12.52979669;
	setAttr ".LeftFootPinky2Ty" 1.8880792420000001;
	setAttr ".LeftFootPinky2Tz" 14.5796458;
	setAttr ".LeftFootPinky3Tx" 12.52979669;
	setAttr ".LeftFootPinky3Ty" 1.8880792289999999;
	setAttr ".LeftFootPinky3Tz" 16.143599309999999;
	setAttr ".LeftFootPinky4Tx" 12.5297967;
	setAttr ".LeftFootPinky4Ty" 1.8880792129999999;
	setAttr ".LeftFootPinky4Tz" 17.861196199999998;
	setAttr ".LeftFootExtraFinger1Tx" 5.0860939849999998;
	setAttr ".LeftFootExtraFinger1Ty" 1.888079254;
	setAttr ".LeftFootExtraFinger1Tz" 12.9547209;
	setAttr ".LeftFootExtraFinger2Tx" 5.0860939910000003;
	setAttr ".LeftFootExtraFinger2Ty" 1.888079236;
	setAttr ".LeftFootExtraFinger2Tz" 14.94401483;
	setAttr ".LeftFootExtraFinger3Tx" 5.0860939979999999;
	setAttr ".LeftFootExtraFinger3Ty" 1.8880792179999999;
	setAttr ".LeftFootExtraFinger3Tz" 16.99182682;
	setAttr ".LeftFootExtraFinger4Tx" 5.0860940049999996;
	setAttr ".LeftFootExtraFinger4Ty" 1.8880791990000001;
	setAttr ".LeftFootExtraFinger4Tz" 19.0793827;
	setAttr ".RightFootThumb1Tx" -6.18422217;
	setAttr ".RightFootThumb1Ty" 4.9992492679999998;
	setAttr ".RightFootThumb1Tz" 1.930123209;
	setAttr ".RightFootThumb2Tx" -4.551409713;
	setAttr ".RightFootThumb2Ty" 2.6643834059999998;
	setAttr ".RightFootThumb2Tz" 3.591937658;
	setAttr ".RightFootThumb3Tx" -3.4619466889999999;
	setAttr ".RightFootThumb3Ty" 1.8880788850000001;
	setAttr ".RightFootThumb3Tz" 6.4001420700000002;
	setAttr ".RightFootThumb4Tx" -3.4619466999999999;
	setAttr ".RightFootThumb4Ty" 1.8880788550000001;
	setAttr ".RightFootThumb4Tz" 9.6971958839999992;
	setAttr ".RightFootIndex1Tx" -7.1105199679999966;
	setAttr ".RightFootIndex1Ty" 1.8880791170000002;
	setAttr ".RightFootIndex1Tz" 12.954720899999998;
	setAttr ".RightFootIndex2Tx" -7.1105199749999999;
	setAttr ".RightFootIndex2Ty" 1.8880790999999983;
	setAttr ".RightFootIndex2Tz" 14.829727449999996;
	setAttr ".RightFootIndex3Tx" -7.1105199809999995;
	setAttr ".RightFootIndex3Ty" 1.888079083;
	setAttr ".RightFootIndex3Tz" 16.763144419999996;
	setAttr ".RightFootIndex4Tx" -7.1105199879999992;
	setAttr ".RightFootIndex4Ty" 1.8880790649999999;
	setAttr ".RightFootIndex4Tz" 18.850666449999999;
	setAttr ".RightFootMiddle1Tx" -8.9167242489998664;
	setAttr ".RightFootMiddle1Ty" 1.8880791629999871;
	setAttr ".RightFootMiddle1Tz" 11.125471607836859;
	setAttr ".RightFootMiddle1Rx" 112.03281418775205;
	setAttr ".RightFootMiddle1Ry" -22.253676258943976;
	setAttr ".RightFootMiddle1Rz" 92.329377997070793;
	setAttr ".RightFootMiddle1Sx" 1.0000000000000004;
	setAttr ".RightFootMiddle1Sy" 1.0000000000000007;
	setAttr ".RightFootMiddle1Sz" 1.0000000000000002;
	setAttr ".RightFootMiddle1JointOrientx" 12.513093810485467;
	setAttr ".RightFootMiddle1JointOrienty" 21.71474579374058;
	setAttr ".RightFootMiddle1JointOrientz" -23.671452349192997;
	setAttr ".RightFootMiddle1MinRLimitx" -45;
	setAttr ".RightFootMiddle1MinRLimity" -45;
	setAttr ".RightFootMiddle1MinRLimitz" -45;
	setAttr ".RightFootMiddle1MaxRLimitx" 45;
	setAttr ".RightFootMiddle1MaxRLimity" 45;
	setAttr ".RightFootMiddle1MaxRLimitz" 45;
	setAttr ".RightFootMiddle2Tx" -8.9167242549998011;
	setAttr ".RightFootMiddle2Ty" 1.8880791531708834;
	setAttr ".RightFootMiddle2Tz" 16.035883306077423;
	setAttr ".RightFootMiddle2Rx" 167.69283632355376;
	setAttr ".RightFootMiddle2Ry" 51.524731383171051;
	setAttr ".RightFootMiddle2Rz" 154.742963129001;
	setAttr ".RightFootMiddle2Sx" 1.0000000000000007;
	setAttr ".RightFootMiddle2Sz" 1.0000000000000007;
	setAttr ".RightFootMiddle2JointOrientx" 22.195611240551923;
	setAttr ".RightFootMiddle2JointOrienty" 11.444985261814127;
	setAttr ".RightFootMiddle2JointOrientz" -91.743537732234685;
	setAttr ".RightFootMiddle2MinRLimitx" -45;
	setAttr ".RightFootMiddle2MinRLimity" -45;
	setAttr ".RightFootMiddle2MinRLimitz" -45;
	setAttr ".RightFootMiddle2MaxRLimitx" 45;
	setAttr ".RightFootMiddle2MaxRLimity" 45;
	setAttr ".RightFootMiddle2MaxRLimitz" 45;
	setAttr ".RightFootMiddle3Tx" -8.9167242610000006;
	setAttr ".RightFootMiddle3Ty" 1.888079131;
	setAttr ".RightFootMiddle3Tz" 16.64971237;
	setAttr ".RightFootMiddle4Tx" -8.9167242669999993;
	setAttr ".RightFootMiddle4Ty" 1.8880791139999999;
	setAttr ".RightFootMiddle4Tz" 18.565581959999999;
	setAttr ".RightFootRing1Tx" -10.723903740000003;
	setAttr ".RightFootRing1Ty" 1.8880792109999991;
	setAttr ".RightFootRing1Tz" 12.9547209;
	setAttr ".RightFootRing2Tx" -10.723903740000003;
	setAttr ".RightFootRing2Ty" 1.888079195;
	setAttr ".RightFootRing2Tz" 14.713452259999999;
	setAttr ".RightFootRing3Tx" -10.723903750000002;
	setAttr ".RightFootRing3Ty" 1.8880791800000001;
	setAttr ".RightFootRing3Tz" 16.472174209999999;
	setAttr ".RightFootRing4Tx" -10.723903760000002;
	setAttr ".RightFootRing4Ty" 1.8880791640000001;
	setAttr ".RightFootRing4Tz" 18.27484922;
	setAttr ".RightFootPinky1Tx" -12.52979668;
	setAttr ".RightFootPinky1Ty" 1.888079257;
	setAttr ".RightFootPinky1Tz" 12.9547209;
	setAttr ".RightFootPinky2Tx" -12.52979669;
	setAttr ".RightFootPinky2Ty" 1.8880792420000001;
	setAttr ".RightFootPinky2Tz" 14.5796458;
	setAttr ".RightFootPinky3Tx" -12.52979669;
	setAttr ".RightFootPinky3Ty" 1.8880792289999999;
	setAttr ".RightFootPinky3Tz" 16.143599309999999;
	setAttr ".RightFootPinky4Tx" -12.5297967;
	setAttr ".RightFootPinky4Ty" 1.8880792129999999;
	setAttr ".RightFootPinky4Tz" 17.861196199999998;
	setAttr ".RightFootExtraFinger1Tx" -5.0860939849999998;
	setAttr ".RightFootExtraFinger1Ty" 1.888079254;
	setAttr ".RightFootExtraFinger1Tz" 12.9547209;
	setAttr ".RightFootExtraFinger2Tx" -5.0860939910000003;
	setAttr ".RightFootExtraFinger2Ty" 1.888079236;
	setAttr ".RightFootExtraFinger2Tz" 14.94401483;
	setAttr ".RightFootExtraFinger3Tx" -5.0860939979999999;
	setAttr ".RightFootExtraFinger3Ty" 1.8880792179999999;
	setAttr ".RightFootExtraFinger3Tz" 16.99182682;
	setAttr ".RightFootExtraFinger4Tx" -5.0860940049999996;
	setAttr ".RightFootExtraFinger4Ty" 1.8880791990000001;
	setAttr ".RightFootExtraFinger4Tz" 19.0793827;
	setAttr ".LeftInHandThumbTx" 71.709864199999998;
	setAttr ".LeftInHandThumbTy" 146.58868419999993;
	setAttr ".LeftInHandIndexTx" 71.709864200000027;
	setAttr ".LeftInHandIndexTy" 146.58868419999996;
	setAttr ".LeftInHandIndexTz" 2.2204460492503131e-016;
	setAttr ".LeftInHandMiddleTx" 71.709864200000027;
	setAttr ".LeftInHandMiddleTy" 146.58868419999996;
	setAttr ".LeftInHandMiddleTz" 2.2204460492503131e-016;
	setAttr ".LeftInHandRingTx" 71.709864200000027;
	setAttr ".LeftInHandRingTy" 146.58868419999996;
	setAttr ".LeftInHandRingTz" 2.2204460492503131e-016;
	setAttr ".LeftInHandPinkyTx" 71.709864200000027;
	setAttr ".LeftInHandPinkyTy" 146.58868419999996;
	setAttr ".LeftInHandPinkyTz" 2.2204460492503131e-016;
	setAttr ".LeftInHandExtraFingerTx" 71.709864199999998;
	setAttr ".LeftInHandExtraFingerTy" 146.58868419999999;
	setAttr ".RightInHandThumbTx" -71.709864199999998;
	setAttr ".RightInHandThumbTy" 146.58868419999993;
	setAttr ".RightInHandIndexTx" -71.709864200000027;
	setAttr ".RightInHandIndexTy" 146.58868419999996;
	setAttr ".RightInHandIndexTz" 2.2204460492503131e-016;
	setAttr ".RightInHandMiddleTx" -71.709864200000027;
	setAttr ".RightInHandMiddleTy" 146.58868419999996;
	setAttr ".RightInHandMiddleTz" 2.2204460492503131e-016;
	setAttr ".RightInHandRingTx" -71.709864200000027;
	setAttr ".RightInHandRingTy" 146.58868419999996;
	setAttr ".RightInHandRingTz" 2.2204460492503131e-016;
	setAttr ".RightInHandPinkyTx" -71.709864200000027;
	setAttr ".RightInHandPinkyTy" 146.58868419999996;
	setAttr ".RightInHandPinkyTz" 2.2204460492503131e-016;
	setAttr ".RightInHandExtraFingerTx" -71.709864199999998;
	setAttr ".RightInHandExtraFingerTy" 146.58868419999999;
	setAttr ".LeftInFootThumbTx" 8.9100008010000007;
	setAttr ".LeftInFootThumbTy" 8.15039625;
	setAttr ".LeftInFootIndexTx" 8.9100008009999989;
	setAttr ".LeftInFootIndexTy" 8.1503963469999974;
	setAttr ".LeftInFootIndexTz" -1.7763568394002505e-015;
	setAttr ".LeftInFootMiddleTx" 8.9100008010000007;
	setAttr ".LeftInFootMiddleTy" 8.1503963469999992;
	setAttr ".LeftInFootRingTx" 8.9100008010000007;
	setAttr ".LeftInFootRingTy" 8.1503963469999992;
	setAttr ".LeftInFootPinkyTx" 8.9100008010000007;
	setAttr ".LeftInFootPinkyTy" 8.1503963469999992;
	setAttr ".LeftInFootExtraFingerTx" 8.9100008010000007;
	setAttr ".LeftInFootExtraFingerTy" 8.1503963469999992;
	setAttr ".RightInFootThumbTx" -8.9100008010000007;
	setAttr ".RightInFootThumbTy" 8.15039625;
	setAttr ".RightInFootIndexTx" -8.9100008009999989;
	setAttr ".RightInFootIndexTy" 8.1503963469999974;
	setAttr ".RightInFootIndexTz" -1.7763568394002505e-015;
	setAttr ".RightInFootMiddleTx" -8.9100008010000007;
	setAttr ".RightInFootMiddleTy" 8.1503963469999992;
	setAttr ".RightInFootRingTx" -8.9100008010000007;
	setAttr ".RightInFootRingTy" 8.1503963469999992;
	setAttr ".RightInFootPinkyTx" -8.9100008010000007;
	setAttr ".RightInFootPinkyTy" 8.1503963469999992;
	setAttr ".RightInFootExtraFingerTx" -8.9100008010000007;
	setAttr ".RightInFootExtraFingerTy" 8.1503963469999992;
	setAttr ".LeftShoulderExtraTx" 12.353625535000001;
	setAttr ".LeftShoulderExtraTy" 146.58868419999999;
	setAttr ".RightShoulderExtraTx" -12.353625535000001;
	setAttr ".RightShoulderExtraTy" 146.58868419999999;
createNode HIKProperty2State -n "HIKproperties1";
	setAttr ".lhr" 1;
	setAttr ".lkr" 1;
	setAttr ".rhr" 1;
	setAttr ".rkr" 1;
	setAttr ".lsr" 1;
	setAttr ".ler" 1;
	setAttr ".rsr" 1;
	setAttr ".rer" 1;
	setAttr ".LeftUpLegRollEx" 1;
	setAttr ".LeftLegRollEx" 1;
	setAttr ".RightUpLegRollEx" 1;
	setAttr ".RightLegRollEx" 1;
	setAttr ".LeftArmRollEx" 1;
	setAttr ".LeftForeArmRollEx" 1;
	setAttr ".RightArmRollEx" 1;
	setAttr ".RightForeArmRollEx" 1;
createNode HIKSkeletonGeneratorNode -n "HIKSkeletonGeneratorNode1";
	setAttr ".ihi" 0;
	setAttr ".SpineCount" 1;
	setAttr ".WantIndexFinger" yes;
	setAttr ".WantMiddleFinger" yes;
	setAttr ".WantRingFinger" yes;
	setAttr ".WantPinkyFinger" yes;
	setAttr ".WantThumb" yes;
	setAttr ".WantMiddleToe" yes;
	setAttr ".WantToeBase" yes;
	setAttr ".ToeJointCount" 1;
	setAttr ".HipsTy" 100;
	setAttr ".LeftUpLegTx" 8.9100008010000025;
	setAttr ".LeftUpLegTy" 93.729999539999994;
	setAttr ".LeftLegTx" 9.6088187334525248;
	setAttr ".LeftLegTy" 48.85135459999988;
	setAttr ".LeftLegTz" 5.3627282272528483;
	setAttr ".LeftFootTx" 8.9100008010000753;
	setAttr ".LeftFootTy" 8.1503963469999832;
	setAttr ".LeftFootTz" -7.1054273576010019e-015;
	setAttr ".RightUpLegTx" -8.9100008010000025;
	setAttr ".RightUpLegTy" 93.729999539999994;
	setAttr ".RightLegTx" -9.6088187334525248;
	setAttr ".RightLegTy" 48.85135459999988;
	setAttr ".RightLegTz" 5.3627282272528483;
	setAttr ".RightFootTx" -8.9100008010000753;
	setAttr ".RightFootTy" 8.1503963469999832;
	setAttr ".RightFootTz" -7.1054273576010019e-015;
	setAttr ".SpineTx" -7.1054273576010019e-015;
	setAttr ".SpineTy" 144.16491502573527;
	setAttr ".LeftArmTx" 17.707251069999948;
	setAttr ".LeftArmTy" 146.58868419999993;
	setAttr ".LeftForeArmTx" 45.012716769999919;
	setAttr ".LeftForeArmTy" 150.00288216303827;
	setAttr ".LeftForeArmTz" -5.3157354550311027;
	setAttr ".LeftHandTx" 71.709864140000064;
	setAttr ".LeftHandTy" 146.58868419999976;
	setAttr ".LeftHandTz" 4.4408920985006262e-015;
	setAttr ".RightArmTx" -17.707251069999948;
	setAttr ".RightArmTy" 146.58868419999993;
	setAttr ".RightForeArmTx" -45.012716769999919;
	setAttr ".RightForeArmTy" 150.00288216303827;
	setAttr ".RightForeArmTz" -5.3157354550311027;
	setAttr ".RightHandTx" -71.709864140000064;
	setAttr ".RightHandTy" 146.58868419999976;
	setAttr ".RightHandTz" 4.4408920985006262e-015;
	setAttr ".HeadTx" -4.4408920985006262e-015;
	setAttr ".HeadTy" 165.00000000000006;
	setAttr ".LeftToeBaseTx" 8.9100092279999572;
	setAttr ".LeftToeBaseTy" 1.8880791539999908;
	setAttr ".LeftToeBaseTz" 6.8367108973667534;
	setAttr ".RightToeBaseTx" -8.9100092279999572;
	setAttr ".RightToeBaseTy" 1.8880791539999908;
	setAttr ".RightToeBaseTz" 6.8367108973667534;
	setAttr ".LeftShoulderTx" 7.0000004769999098;
	setAttr ".LeftShoulderTy" 146.58854679999999;
	setAttr ".RightShoulderTx" -7.0000004769999098;
	setAttr ".RightShoulderTy" 146.58854679999999;
	setAttr ".NeckTx" -1.6875389974302379e-013;
	setAttr ".NeckTy" 153.971843256429;
	setAttr ".LeftFingerBaseTx" 80.519743440000028;
	setAttr ".LeftFingerBaseTy" 147.08957459999999;
	setAttr ".LeftFingerBaseTz" 1.304684401;
	setAttr ".RightFingerBaseTx" -80.519743440000028;
	setAttr ".RightFingerBaseTy" 147.08957459999999;
	setAttr ".RightFingerBaseTz" 1.304684401;
	setAttr ".Spine1Ty" 119.66666666666667;
	setAttr ".Spine2Ty" 132.33333333333334;
	setAttr ".Spine3Ty" 119;
	setAttr ".Spine4Ty" 123;
	setAttr ".Spine5Ty" 127;
	setAttr ".Spine6Ty" 131;
	setAttr ".Spine7Ty" 135;
	setAttr ".Spine8Ty" 139;
	setAttr ".Spine9Ty" 143;
	setAttr ".Neck1Tx" 2.2204460492503131e-015;
	setAttr ".Neck1Ty" 159.4859216282145;
	setAttr ".Neck2Ty" 149;
	setAttr ".Neck3Ty" 151;
	setAttr ".Neck4Ty" 153;
	setAttr ".Neck5Ty" 155;
	setAttr ".Neck6Ty" 157;
	setAttr ".Neck7Ty" 159;
	setAttr ".Neck8Ty" 161;
	setAttr ".Neck9Ty" 163;
	setAttr ".LeftUpLegRollTx" 9.2594097672262627;
	setAttr ".LeftUpLegRollTy" 71.29067706999993;
	setAttr ".LeftUpLegRollTz" 2.6813641136264241;
	setAttr ".LeftLegRollTx" 9.2594097672263;
	setAttr ".LeftLegRollTy" 28.500875473499931;
	setAttr ".LeftLegRollTz" 2.6813641136264206;
	setAttr ".RightUpLegRollTx" -9.2594097672262627;
	setAttr ".RightUpLegRollTy" 71.29067706999993;
	setAttr ".RightUpLegRollTz" 2.6813641136264241;
	setAttr ".RightLegRollTx" -9.2594097672263;
	setAttr ".RightLegRollTy" 28.500875473499931;
	setAttr ".RightLegRollTz" 2.6813641136264206;
	setAttr ".LeftArmRollTx" 31.359983919999934;
	setAttr ".LeftArmRollTy" 148.29578318151908;
	setAttr ".LeftArmRollTz" -2.6578677275155513;
	setAttr ".LeftForeArmRollTx" 58.361290454999988;
	setAttr ".LeftForeArmRollTy" 148.29578318151903;
	setAttr ".LeftForeArmRollTz" -2.6578677275155491;
	setAttr ".RightArmRollTx" -31.359983919999934;
	setAttr ".RightArmRollTy" 148.29578318151908;
	setAttr ".RightArmRollTz" -2.6578677275155513;
	setAttr ".RightForeArmRollTx" -58.361290454999988;
	setAttr ".RightForeArmRollTy" 148.29578318151903;
	setAttr ".RightForeArmRollTz" -2.6578677275155491;
	setAttr ".HipsTranslationTy" 100;
	setAttr ".LeftHandThumb1Tx" 76.058620990000094;
	setAttr ".LeftHandThumb1Ty" 145.79018169999998;
	setAttr ".LeftHandThumb1Tz" 4.2824339669999976;
	setAttr ".LeftHandThumb2Tx" 78.57121093000012;
	setAttr ".LeftHandThumb2Ty" 145.25408229999996;
	setAttr ".LeftHandThumb2Tz" 4.9898882909999784;
	setAttr ".LeftHandThumb3Tx" 81.114351340000141;
	setAttr ".LeftHandThumb3Ty" 145.2540690999999;
	setAttr ".LeftHandThumb3Tz" 4.9898976329999902;
	setAttr ".LeftHandThumb4Tx" 83.781097480000085;
	setAttr ".LeftHandThumb4Ty" 145.25407199999989;
	setAttr ".LeftHandThumb4Tz" 4.9898894219999752;
	setAttr ".LeftHandIndex1Tx" 80.531840859999974;
	setAttr ".LeftHandIndex1Ty" 146.78841339999991;
	setAttr ".LeftHandIndex1Tz" 3.4716694159999815;
	setAttr ".LeftHandIndex2Tx" 84.75459546000009;
	setAttr ".LeftHandIndex2Ty" 146.7883913;
	setAttr ".LeftHandIndex2Tz" 3.61886843499998;
	setAttr ".LeftHandIndex3Tx" 87.406920909999968;
	setAttr ".LeftHandIndex3Ty" 146.78837750000051;
	setAttr ".LeftHandIndex3Tz" 3.7113244149999778;
	setAttr ".LeftHandIndex4Tx" 89.363955140000272;
	setAttr ".LeftHandIndex4Ty" 146.78836729999998;
	setAttr ".LeftHandIndex4Tz" 3.7795433149999891;
	setAttr ".LeftHandMiddle1Tx" 80.519743500000033;
	setAttr ".LeftHandMiddle1Ty" 147.0895747000001;
	setAttr ".LeftHandMiddle1Tz" 1.3046843809999804;
	setAttr ".LeftHandMiddle2Tx" 85.382995179999952;
	setAttr ".LeftHandMiddle2Ty" 147.08957469999979;
	setAttr ".LeftHandMiddle2Tz" 1.3049868359999799;
	setAttr ".LeftHandMiddle3Tx" 88.148231789999869;
	setAttr ".LeftHandMiddle3Ty" 147.0895746999997;
	setAttr ".LeftHandMiddle3Tz" 1.3051586189999691;
	setAttr ".LeftHandMiddle4Tx" 90.153863950000002;
	setAttr ".LeftHandMiddle4Ty" 147.08957469999976;
	setAttr ".LeftHandMiddle4Tz" 1.3052822149999905;
	setAttr ".LeftHandRing1Tx" 80.603623929999927;
	setAttr ".LeftHandRing1Ty" 146.96860380000007;
	setAttr ".LeftHandRing1Tz" -0.79315890900001285;
	setAttr ".LeftHandRing2Tx" 85.141382760000056;
	setAttr ".LeftHandRing2Ty" 146.96860379999987;
	setAttr ".LeftHandRing2Tz" -0.7931588200000228;
	setAttr ".LeftHandRing3Tx" 87.445908620000012;
	setAttr ".LeftHandRing3Ty" 146.96860379999998;
	setAttr ".LeftHandRing3Tz" -0.79315893700001672;
	setAttr ".LeftHandRing4Tx" 89.369255979999991;
	setAttr ".LeftHandRing4Ty" 146.96860379999993;
	setAttr ".LeftHandRing4Tz" -0.79315975400002414;
	setAttr ".LeftHandPinky1Tx" 80.592138830000053;
	setAttr ".LeftHandPinky1Ty" 146.27565720000021;
	setAttr ".LeftHandPinky1Tz" -2.4903564650000058;
	setAttr ".LeftHandPinky2Tx" 83.636238160000161;
	setAttr ".LeftHandPinky2Ty" 146.27569780000013;
	setAttr ".LeftHandPinky2Tz" -2.4903564650000214;
	setAttr ".LeftHandPinky3Tx" 85.610739649999942;
	setAttr ".LeftHandPinky3Ty" 146.27572409999974;
	setAttr ".LeftHandPinky3Tz" -2.4903566080000319;
	setAttr ".LeftHandPinky4Tx" 87.277354300000098;
	setAttr ".LeftHandPinky4Ty" 146.27574629999998;
	setAttr ".LeftHandPinky4Tz" -2.4903558170000095;
	setAttr ".LeftHandExtraFinger1Tx" 80.592138829999996;
	setAttr ".LeftHandExtraFinger1Ty" 146.7884134;
	setAttr ".LeftHandExtraFinger1Tz" -4.4903564649999996;
	setAttr ".LeftHandExtraFinger1Ry" -1.9999999850000001;
	setAttr ".LeftHandExtraFinger1Rz" -0.00029934100000000001;
	setAttr ".LeftHandExtraFinger2Tx" 82.636238160000005;
	setAttr ".LeftHandExtraFinger2Ty" 146.7883913;
	setAttr ".LeftHandExtraFinger2Tz" -4.4903564649999996;
	setAttr ".LeftHandExtraFinger2Ry" -1.9999999850000001;
	setAttr ".LeftHandExtraFinger2Rz" -0.00029934100000000001;
	setAttr ".LeftHandExtraFinger3Tx" 84.610739649999999;
	setAttr ".LeftHandExtraFinger3Ty" 146.7883775;
	setAttr ".LeftHandExtraFinger3Tz" -4.4903566079999999;
	setAttr ".LeftHandExtraFinger3Ry" -1.9999999850000001;
	setAttr ".LeftHandExtraFinger3Rz" -0.00029934100000000001;
	setAttr ".LeftHandExtraFinger4Tx" 86.277354299999999;
	setAttr ".LeftHandExtraFinger4Ty" 146.7883673;
	setAttr ".LeftHandExtraFinger4Tz" -4.4903558170000002;
	setAttr ".LeftHandExtraFinger4Ry" -1.9999999850000001;
	setAttr ".LeftHandExtraFinger4Rz" -0.00029934100000000001;
	setAttr ".RightHandThumb1Tx" -76.058620990000094;
	setAttr ".RightHandThumb1Ty" 145.79018169999998;
	setAttr ".RightHandThumb1Tz" 4.2824339669999976;
	setAttr ".RightHandThumb2Tx" -78.57121093000012;
	setAttr ".RightHandThumb2Ty" 145.25408229999996;
	setAttr ".RightHandThumb2Tz" 4.9898882909999784;
	setAttr ".RightHandThumb3Tx" -81.114351340000141;
	setAttr ".RightHandThumb3Ty" 145.2540690999999;
	setAttr ".RightHandThumb3Tz" 4.9898976329999902;
	setAttr ".RightHandThumb4Tx" -83.781097480000085;
	setAttr ".RightHandThumb4Ty" 145.25407199999989;
	setAttr ".RightHandThumb4Tz" 4.9898894219999752;
	setAttr ".RightHandIndex1Tx" -80.531840859999974;
	setAttr ".RightHandIndex1Ty" 146.78841339999991;
	setAttr ".RightHandIndex1Tz" 3.4716694159999815;
	setAttr ".RightHandIndex2Tx" -84.75459546000009;
	setAttr ".RightHandIndex2Ty" 146.7883913;
	setAttr ".RightHandIndex2Tz" 3.61886843499998;
	setAttr ".RightHandIndex3Tx" -87.406920909999968;
	setAttr ".RightHandIndex3Ty" 146.78837750000051;
	setAttr ".RightHandIndex3Tz" 3.7113244149999778;
	setAttr ".RightHandIndex4Tx" -89.363955140000272;
	setAttr ".RightHandIndex4Ty" 146.78836729999998;
	setAttr ".RightHandIndex4Tz" 3.7795433149999891;
	setAttr ".RightHandMiddle1Tx" -80.519743500000033;
	setAttr ".RightHandMiddle1Ty" 147.0895747000001;
	setAttr ".RightHandMiddle1Tz" 1.3046843809999804;
	setAttr ".RightHandMiddle2Tx" -85.382995179999952;
	setAttr ".RightHandMiddle2Ty" 147.08957469999979;
	setAttr ".RightHandMiddle2Tz" 1.3049868359999799;
	setAttr ".RightHandMiddle3Tx" -88.148231789999869;
	setAttr ".RightHandMiddle3Ty" 147.0895746999997;
	setAttr ".RightHandMiddle3Tz" 1.3051586189999691;
	setAttr ".RightHandMiddle4Tx" -90.153863950000002;
	setAttr ".RightHandMiddle4Ty" 147.08957469999976;
	setAttr ".RightHandMiddle4Tz" 1.3052822149999905;
	setAttr ".RightHandRing1Tx" -80.603623929999927;
	setAttr ".RightHandRing1Ty" 146.96860380000007;
	setAttr ".RightHandRing1Tz" -0.79315890900001285;
	setAttr ".RightHandRing2Tx" -85.141382760000056;
	setAttr ".RightHandRing2Ty" 146.96860379999987;
	setAttr ".RightHandRing2Tz" -0.7931588200000228;
	setAttr ".RightHandRing3Tx" -87.445908620000012;
	setAttr ".RightHandRing3Ty" 146.96860379999998;
	setAttr ".RightHandRing3Tz" -0.79315893700001672;
	setAttr ".RightHandRing4Tx" -89.369255979999991;
	setAttr ".RightHandRing4Ty" 146.96860379999993;
	setAttr ".RightHandRing4Tz" -0.79315975400002414;
	setAttr ".RightHandPinky1Tx" -80.592138830000053;
	setAttr ".RightHandPinky1Ty" 146.27565720000021;
	setAttr ".RightHandPinky1Tz" -2.4903564650000058;
	setAttr ".RightHandPinky2Tx" -83.636238160000161;
	setAttr ".RightHandPinky2Ty" 146.27569780000013;
	setAttr ".RightHandPinky2Tz" -2.4903564650000214;
	setAttr ".RightHandPinky3Tx" -85.610739649999942;
	setAttr ".RightHandPinky3Ty" 146.27572409999974;
	setAttr ".RightHandPinky3Tz" -2.4903566080000319;
	setAttr ".RightHandPinky4Tx" -87.277354300000098;
	setAttr ".RightHandPinky4Ty" 146.27574629999998;
	setAttr ".RightHandPinky4Tz" -2.4903558170000095;
	setAttr ".RightHandExtraFinger1Tx" -80.592138829999996;
	setAttr ".RightHandExtraFinger1Ty" 146.7884134;
	setAttr ".RightHandExtraFinger1Tz" -4.4903564649999996;
	setAttr ".RightHandExtraFinger1Ry" -2.0000646579999999;
	setAttr ".RightHandExtraFinger2Tx" -82.636238160000005;
	setAttr ".RightHandExtraFinger2Ty" 146.7883913;
	setAttr ".RightHandExtraFinger2Tz" -4.4903564649999996;
	setAttr ".RightHandExtraFinger2Ry" -2.0000646359999998;
	setAttr ".RightHandExtraFinger3Tx" -84.610739649999999;
	setAttr ".RightHandExtraFinger3Ty" 146.7883775;
	setAttr ".RightHandExtraFinger3Tz" -4.4903566079999999;
	setAttr ".RightHandExtraFinger3Ry" -2.0000646359999998;
	setAttr ".RightHandExtraFinger4Tx" -86.277354299999999;
	setAttr ".RightHandExtraFinger4Ty" 146.7883673;
	setAttr ".RightHandExtraFinger4Tz" -4.4903558170000002;
	setAttr ".RightHandExtraFinger4Ry" -2.0000646359999998;
	setAttr ".LeftFootThumb1Tx" 6.18422217;
	setAttr ".LeftFootThumb1Ty" 4.9992492679999998;
	setAttr ".LeftFootThumb1Tz" 1.930123209;
	setAttr ".LeftFootThumb2Tx" 4.551409713;
	setAttr ".LeftFootThumb2Ty" 2.6643834059999998;
	setAttr ".LeftFootThumb2Tz" 3.591937658;
	setAttr ".LeftFootThumb3Tx" 3.4619466889999999;
	setAttr ".LeftFootThumb3Ty" 1.8880788850000001;
	setAttr ".LeftFootThumb3Tz" 6.4001420700000002;
	setAttr ".LeftFootThumb4Tx" 3.4619466999999999;
	setAttr ".LeftFootThumb4Ty" 1.8880788550000001;
	setAttr ".LeftFootThumb4Tz" 9.6971958839999992;
	setAttr ".LeftFootIndex1Tx" 7.1105199679999966;
	setAttr ".LeftFootIndex1Ty" 1.8880791170000002;
	setAttr ".LeftFootIndex1Tz" 12.954720899999998;
	setAttr ".LeftFootIndex2Tx" 7.1105199749999999;
	setAttr ".LeftFootIndex2Ty" 1.8880790999999983;
	setAttr ".LeftFootIndex2Tz" 14.829727449999996;
	setAttr ".LeftFootIndex3Tx" 7.1105199809999995;
	setAttr ".LeftFootIndex3Ty" 1.888079083;
	setAttr ".LeftFootIndex3Tz" 16.763144419999996;
	setAttr ".LeftFootIndex4Tx" 7.1105199879999992;
	setAttr ".LeftFootIndex4Ty" 1.8880790649999999;
	setAttr ".LeftFootIndex4Tz" 18.850666449999999;
	setAttr ".LeftFootMiddle1Tx" 8.9167242489998646;
	setAttr ".LeftFootMiddle1Ty" 1.8880791629999878;
	setAttr ".LeftFootMiddle1Tz" 11.125471607836857;
	setAttr ".LeftFootMiddle2Tx" 8.9167242549997994;
	setAttr ".LeftFootMiddle2Ty" 1.8880791531708854;
	setAttr ".LeftFootMiddle2Tz" 16.03588330607742;
	setAttr ".LeftFootMiddle3Tx" 8.9167242610000006;
	setAttr ".LeftFootMiddle3Ty" 1.888079131;
	setAttr ".LeftFootMiddle3Tz" 16.64971237;
	setAttr ".LeftFootMiddle4Tx" 8.9167242669999993;
	setAttr ".LeftFootMiddle4Ty" 1.8880791139999999;
	setAttr ".LeftFootMiddle4Tz" 18.565581959999999;
	setAttr ".LeftFootRing1Tx" 10.723903740000003;
	setAttr ".LeftFootRing1Ty" 1.8880792109999991;
	setAttr ".LeftFootRing1Tz" 12.9547209;
	setAttr ".LeftFootRing2Tx" 10.723903740000003;
	setAttr ".LeftFootRing2Ty" 1.888079195;
	setAttr ".LeftFootRing2Tz" 14.713452259999999;
	setAttr ".LeftFootRing3Tx" 10.723903750000002;
	setAttr ".LeftFootRing3Ty" 1.8880791800000001;
	setAttr ".LeftFootRing3Tz" 16.472174209999999;
	setAttr ".LeftFootRing4Tx" 10.723903760000002;
	setAttr ".LeftFootRing4Ty" 1.8880791640000001;
	setAttr ".LeftFootRing4Tz" 18.27484922;
	setAttr ".LeftFootPinky1Tx" 12.52979668;
	setAttr ".LeftFootPinky1Ty" 1.888079257;
	setAttr ".LeftFootPinky1Tz" 12.9547209;
	setAttr ".LeftFootPinky2Tx" 12.52979669;
	setAttr ".LeftFootPinky2Ty" 1.8880792420000001;
	setAttr ".LeftFootPinky2Tz" 14.5796458;
	setAttr ".LeftFootPinky3Tx" 12.52979669;
	setAttr ".LeftFootPinky3Ty" 1.8880792289999999;
	setAttr ".LeftFootPinky3Tz" 16.143599309999999;
	setAttr ".LeftFootPinky4Tx" 12.5297967;
	setAttr ".LeftFootPinky4Ty" 1.8880792129999999;
	setAttr ".LeftFootPinky4Tz" 17.861196199999998;
	setAttr ".LeftFootExtraFinger1Tx" 5.0860939849999998;
	setAttr ".LeftFootExtraFinger1Ty" 1.888079254;
	setAttr ".LeftFootExtraFinger1Tz" 12.9547209;
	setAttr ".LeftFootExtraFinger2Tx" 5.0860939910000003;
	setAttr ".LeftFootExtraFinger2Ty" 1.888079236;
	setAttr ".LeftFootExtraFinger2Tz" 14.94401483;
	setAttr ".LeftFootExtraFinger3Tx" 5.0860939979999999;
	setAttr ".LeftFootExtraFinger3Ty" 1.8880792179999999;
	setAttr ".LeftFootExtraFinger3Tz" 16.99182682;
	setAttr ".LeftFootExtraFinger4Tx" 5.0860940049999996;
	setAttr ".LeftFootExtraFinger4Ty" 1.8880791990000001;
	setAttr ".LeftFootExtraFinger4Tz" 19.0793827;
	setAttr ".RightFootThumb1Tx" -6.18422217;
	setAttr ".RightFootThumb1Ty" 4.9992492679999998;
	setAttr ".RightFootThumb1Tz" 1.930123209;
	setAttr ".RightFootThumb2Tx" -4.551409713;
	setAttr ".RightFootThumb2Ty" 2.6643834059999998;
	setAttr ".RightFootThumb2Tz" 3.591937658;
	setAttr ".RightFootThumb3Tx" -3.4619466889999999;
	setAttr ".RightFootThumb3Ty" 1.8880788850000001;
	setAttr ".RightFootThumb3Tz" 6.4001420700000002;
	setAttr ".RightFootThumb4Tx" -3.4619466999999999;
	setAttr ".RightFootThumb4Ty" 1.8880788550000001;
	setAttr ".RightFootThumb4Tz" 9.6971958839999992;
	setAttr ".RightFootIndex1Tx" -7.1105199679999966;
	setAttr ".RightFootIndex1Ty" 1.8880791170000002;
	setAttr ".RightFootIndex1Tz" 12.954720899999998;
	setAttr ".RightFootIndex2Tx" -7.1105199749999999;
	setAttr ".RightFootIndex2Ty" 1.8880790999999983;
	setAttr ".RightFootIndex2Tz" 14.829727449999996;
	setAttr ".RightFootIndex3Tx" -7.1105199809999995;
	setAttr ".RightFootIndex3Ty" 1.888079083;
	setAttr ".RightFootIndex3Tz" 16.763144419999996;
	setAttr ".RightFootIndex4Tx" -7.1105199879999992;
	setAttr ".RightFootIndex4Ty" 1.8880790649999999;
	setAttr ".RightFootIndex4Tz" 18.850666449999999;
	setAttr ".RightFootMiddle1Tx" -8.9167242489998646;
	setAttr ".RightFootMiddle1Ty" 1.8880791629999878;
	setAttr ".RightFootMiddle1Tz" 11.125471607836857;
	setAttr ".RightFootMiddle2Tx" -8.9167242549997994;
	setAttr ".RightFootMiddle2Ty" 1.8880791531708854;
	setAttr ".RightFootMiddle2Tz" 16.03588330607742;
	setAttr ".RightFootMiddle3Tx" -8.9167242610000006;
	setAttr ".RightFootMiddle3Ty" 1.888079131;
	setAttr ".RightFootMiddle3Tz" 16.64971237;
	setAttr ".RightFootMiddle4Tx" -8.9167242669999993;
	setAttr ".RightFootMiddle4Ty" 1.8880791139999999;
	setAttr ".RightFootMiddle4Tz" 18.565581959999999;
	setAttr ".RightFootRing1Tx" -10.723903740000003;
	setAttr ".RightFootRing1Ty" 1.8880792109999991;
	setAttr ".RightFootRing1Tz" 12.9547209;
	setAttr ".RightFootRing2Tx" -10.723903740000003;
	setAttr ".RightFootRing2Ty" 1.888079195;
	setAttr ".RightFootRing2Tz" 14.713452259999999;
	setAttr ".RightFootRing3Tx" -10.723903750000002;
	setAttr ".RightFootRing3Ty" 1.8880791800000001;
	setAttr ".RightFootRing3Tz" 16.472174209999999;
	setAttr ".RightFootRing4Tx" -10.723903760000002;
	setAttr ".RightFootRing4Ty" 1.8880791640000001;
	setAttr ".RightFootRing4Tz" 18.27484922;
	setAttr ".RightFootPinky1Tx" -12.52979668;
	setAttr ".RightFootPinky1Ty" 1.888079257;
	setAttr ".RightFootPinky1Tz" 12.9547209;
	setAttr ".RightFootPinky2Tx" -12.52979669;
	setAttr ".RightFootPinky2Ty" 1.8880792420000001;
	setAttr ".RightFootPinky2Tz" 14.5796458;
	setAttr ".RightFootPinky3Tx" -12.52979669;
	setAttr ".RightFootPinky3Ty" 1.8880792289999999;
	setAttr ".RightFootPinky3Tz" 16.143599309999999;
	setAttr ".RightFootPinky4Tx" -12.5297967;
	setAttr ".RightFootPinky4Ty" 1.8880792129999999;
	setAttr ".RightFootPinky4Tz" 17.861196199999998;
	setAttr ".RightFootExtraFinger1Tx" -5.0860939849999998;
	setAttr ".RightFootExtraFinger1Ty" 1.888079254;
	setAttr ".RightFootExtraFinger1Tz" 12.9547209;
	setAttr ".RightFootExtraFinger2Tx" -5.0860939910000003;
	setAttr ".RightFootExtraFinger2Ty" 1.888079236;
	setAttr ".RightFootExtraFinger2Tz" 14.94401483;
	setAttr ".RightFootExtraFinger3Tx" -5.0860939979999999;
	setAttr ".RightFootExtraFinger3Ty" 1.8880792179999999;
	setAttr ".RightFootExtraFinger3Tz" 16.99182682;
	setAttr ".RightFootExtraFinger4Tx" -5.0860940049999996;
	setAttr ".RightFootExtraFinger4Ty" 1.8880791990000001;
	setAttr ".RightFootExtraFinger4Tz" 19.0793827;
	setAttr ".LeftInHandThumbTx" 71.709864199999998;
	setAttr ".LeftInHandThumbTy" 146.58868419999993;
	setAttr ".LeftInHandIndexTx" 71.709864200000027;
	setAttr ".LeftInHandIndexTy" 146.58868419999996;
	setAttr ".LeftInHandIndexTz" 2.2204460492503131e-016;
	setAttr ".LeftInHandMiddleTx" 71.709864200000027;
	setAttr ".LeftInHandMiddleTy" 146.58868419999996;
	setAttr ".LeftInHandMiddleTz" 2.2204460492503131e-016;
	setAttr ".LeftInHandRingTx" 71.709864200000027;
	setAttr ".LeftInHandRingTy" 146.58868419999996;
	setAttr ".LeftInHandRingTz" 2.2204460492503131e-016;
	setAttr ".LeftInHandPinkyTx" 71.709864200000027;
	setAttr ".LeftInHandPinkyTy" 146.58868419999996;
	setAttr ".LeftInHandPinkyTz" 2.2204460492503131e-016;
	setAttr ".LeftInHandExtraFingerTx" 71.709864199999998;
	setAttr ".LeftInHandExtraFingerTy" 146.58868419999999;
	setAttr ".RightInHandThumbTx" -71.709864199999998;
	setAttr ".RightInHandThumbTy" 146.58868419999993;
	setAttr ".RightInHandIndexTx" -71.709864200000027;
	setAttr ".RightInHandIndexTy" 146.58868419999996;
	setAttr ".RightInHandIndexTz" 2.2204460492503131e-016;
	setAttr ".RightInHandMiddleTx" -71.709864200000027;
	setAttr ".RightInHandMiddleTy" 146.58868419999996;
	setAttr ".RightInHandMiddleTz" 2.2204460492503131e-016;
	setAttr ".RightInHandRingTx" -71.709864200000027;
	setAttr ".RightInHandRingTy" 146.58868419999996;
	setAttr ".RightInHandRingTz" 2.2204460492503131e-016;
	setAttr ".RightInHandPinkyTx" -71.709864200000027;
	setAttr ".RightInHandPinkyTy" 146.58868419999996;
	setAttr ".RightInHandPinkyTz" 2.2204460492503131e-016;
	setAttr ".RightInHandExtraFingerTx" -71.709864199999998;
	setAttr ".RightInHandExtraFingerTy" 146.58868419999999;
	setAttr ".LeftInFootThumbTx" 8.9100008010000007;
	setAttr ".LeftInFootThumbTy" 8.15039625;
	setAttr ".LeftInFootIndexTx" 8.9100008009999989;
	setAttr ".LeftInFootIndexTy" 8.1503963469999974;
	setAttr ".LeftInFootIndexTz" -1.7763568394002505e-015;
	setAttr ".LeftInFootMiddleTx" 8.9100008010000007;
	setAttr ".LeftInFootMiddleTy" 8.1503963469999992;
	setAttr ".LeftInFootRingTx" 8.9100008010000007;
	setAttr ".LeftInFootRingTy" 8.1503963469999992;
	setAttr ".LeftInFootPinkyTx" 8.9100008010000007;
	setAttr ".LeftInFootPinkyTy" 8.1503963469999992;
	setAttr ".LeftInFootExtraFingerTx" 8.9100008010000007;
	setAttr ".LeftInFootExtraFingerTy" 8.1503963469999992;
	setAttr ".RightInFootThumbTx" -8.9100008010000007;
	setAttr ".RightInFootThumbTy" 8.15039625;
	setAttr ".RightInFootIndexTx" -8.9100008009999989;
	setAttr ".RightInFootIndexTy" 8.1503963469999974;
	setAttr ".RightInFootIndexTz" -1.7763568394002505e-015;
	setAttr ".RightInFootMiddleTx" -8.9100008010000007;
	setAttr ".RightInFootMiddleTy" 8.1503963469999992;
	setAttr ".RightInFootRingTx" -8.9100008010000007;
	setAttr ".RightInFootRingTy" 8.1503963469999992;
	setAttr ".RightInFootPinkyTx" -8.9100008010000007;
	setAttr ".RightInFootPinkyTy" 8.1503963469999992;
	setAttr ".RightInFootExtraFingerTx" -8.9100008010000007;
	setAttr ".RightInFootExtraFingerTy" 8.1503963469999992;
	setAttr ".LeftShoulderExtraTx" 12.353625535000001;
	setAttr ".LeftShoulderExtraTy" 146.58868419999999;
	setAttr ".RightShoulderExtraTx" -12.353625535000001;
	setAttr ".RightShoulderExtraTy" 146.58868419999999;
createNode HIKSolverNode -n "HIKSolverNode1";
	setAttr ".ihi" 0;
	setAttr ".InputStance" yes;
createNode HIKState2SK -n "HIKState2SK1";
	setAttr ".ihi" 0;
createNode script -n "uiConfigurationScriptNode";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n"
		+ "                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n"
		+ "                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n"
		+ "            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n"
		+ "            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n"
		+ "                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n"
		+ "                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n"
		+ "                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n"
		+ "            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n"
		+ "                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n"
		+ "                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n"
		+ "                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n"
		+ "            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n"
		+ "            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n"
		+ "                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n"
		+ "                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n"
		+ "                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n"
		+ "            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n"
		+ "            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n"
		+ "            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showReferenceNodes 1\n                -showReferenceMembers 1\n                -showAttributes 0\n                -showConnected 1\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n"
		+ "                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n"
		+ "                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 1\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n"
		+ "            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n"
		+ "            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n"
		+ "                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n"
		+ "                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n"
		+ "                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n"
		+ "                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n"
		+ "                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n"
		+ "                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n"
		+ "                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n"
		+ "                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n"
		+ "                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n"
		+ "                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n"
		+ "                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy9\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy9\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 0.859365\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n"
		+ "                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 5\n                -currentNode \"Lucas_LeftFootMiddle2\" \n                -opaqueContainers 0\n                -dropNode \"pasted__ControlCabeza\" \n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"largeIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy9\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n"
		+ "                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 0.859365\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 5\n                -currentNode \"Lucas_LeftFootMiddle2\" \n                -opaqueContainers 0\n                -dropNode \"pasted__ControlCabeza\" \n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"largeIcons\" \n"
		+ "                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\tif ($useSceneConfig) {\n\t\tscriptedPanel -e -to $panelName;\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -ignoreAssets 1\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -keyReleaseCommand \"nodeEdKeyReleaseCommand\" \n                -nodeTitleMode \"name\" \n"
		+ "                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -island 0\n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -syncedSelection 1\n                -extendToShapes 1\n                $editorName;\n\t\t\tif (`objExists nodeEditorPanel1Info`) nodeEditor -e -restoreInfo nodeEditorPanel1Info $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -ignoreAssets 1\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n"
		+ "                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -keyReleaseCommand \"nodeEdKeyReleaseCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -island 0\n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -syncedSelection 1\n                -extendToShapes 1\n                $editorName;\n\t\t\tif (`objExists nodeEditorPanel1Info`) nodeEditor -e -restoreInfo nodeEditorPanel1Info $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Texture Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\tif ($useSceneConfig) {\n\t\tscriptedPanel -e -to $panelName;\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"Stereo\" -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels `;\n"
		+ "string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n"
		+ "                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n"
		+ "                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n"
		+ "            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n"
		+ "                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n"
		+ "                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n"
		+ "                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy3\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy3\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 1\n                -zoom 1\n"
		+ "                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy3\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 1\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n"
		+ "                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy1\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy1\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n"
		+ "                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy1\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n"
		+ "                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy2\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy2\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n"
		+ "                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy2\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n"
		+ "                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy4\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy4\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n"
		+ "                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy4\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n"
		+ "                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy5\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy5\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n"
		+ "                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -currentNode \"pasted__V\" \n                -opaqueContainers 0\n                -dropNode \"clav_ctrl\" \n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy5\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n"
		+ "            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -currentNode \"pasted__V\" \n                -opaqueContainers 0\n                -dropNode \"clav_ctrl\" \n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n"
		+ "                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy6\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy6\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n"
		+ "                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy6\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n"
		+ "                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy7\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy7\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n"
		+ "                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy7\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n"
		+ "                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy8\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy8\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n"
		+ "                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 0.773151\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 5\n                -currentNode \"pasted__V\" \n                -opaqueContainers 0\n                -dropNode \"pasted__V\" \n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"largeIcons\" \n"
		+ "                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy8\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 0.773151\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 5\n                -currentNode \"pasted__V\" \n                -opaqueContainers 0\n                -dropNode \"pasted__V\" \n                -freeform 0\n                -imagePosition 0 0 \n"
		+ "                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"largeIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\tif ($useSceneConfig) {\n\t\tscriptedPanel -e -to $panelName;\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Model Panel5\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Model Panel5\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n"
		+ "                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 0\n                -nurbsSurfaces 0\n                -polymeshes 1\n                -subdivSurfaces 0\n                -planes 0\n                -lights 0\n                -cameras 0\n                -controlVertices 0\n                -hulls 0\n                -grid 0\n                -imagePlane 0\n                -joints 0\n                -ikHandles 0\n"
		+ "                -deformers 0\n                -dynamics 0\n                -fluids 0\n                -hairSystems 0\n                -follicles 0\n                -nCloths 0\n                -nParticles 0\n                -nRigids 0\n                -dynamicConstraints 0\n                -locators 0\n                -manipulators 0\n                -pluginShapes 0\n                -dimensions 0\n                -handles 0\n                -pivots 0\n                -textures 0\n                -strokes 0\n                -motionTrails 0\n                -clipGhosts 0\n                -greasePencils 0\n                -shadows 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Model Panel5\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n"
		+ "            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -objectFilterShowInHUD 1\n            -isFiltered 0\n"
		+ "            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 0\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 0\n            -nurbsSurfaces 0\n            -polymeshes 1\n            -subdivSurfaces 0\n            -planes 0\n            -lights 0\n            -cameras 0\n            -controlVertices 0\n            -hulls 0\n            -grid 0\n            -imagePlane 0\n            -joints 0\n            -ikHandles 0\n            -deformers 0\n            -dynamics 0\n            -fluids 0\n            -hairSystems 0\n"
		+ "            -follicles 0\n            -nCloths 0\n            -nParticles 0\n            -nRigids 0\n            -dynamicConstraints 0\n            -locators 0\n            -manipulators 0\n            -pluginShapes 0\n            -dimensions 0\n            -handles 0\n            -pivots 0\n            -textures 0\n            -strokes 0\n            -motionTrails 0\n            -clipGhosts 0\n            -greasePencils 0\n            -shadows 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor2\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor2\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n"
		+ "                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n"
		+ "                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n"
		+ "                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor2\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n"
		+ "                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n"
		+ "                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n"
		+ "                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n"
		+ "\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 24 -ast 1 -aet 48 ";
	setAttr ".st" 6;
createNode displayLayer -n "V2_defaultLayer";
createNode ilrOptionsNode -s -n "TurtleRenderOptions";
lockNode -l 1 ;
createNode ilrUIOptionsNode -s -n "TurtleUIOptions";
lockNode -l 1 ;
createNode ilrBakeLayerManager -s -n "TurtleBakeLayerManager";
lockNode -l 1 ;
createNode ilrBakeLayer -s -n "TurtleDefaultBakeLayer";
lockNode -l 1 ;
createNode hyperGraphInfo -n "nodeEditorPanel1Info";
createNode hyperView -n "hyperView1";
	setAttr ".dag" no;
createNode hyperLayout -n "hyperLayout1";
	setAttr ".ihi" 0;
	setAttr -s 4 ".hyp";
	setAttr ".hyp[0].nvs" 1920;
	setAttr ".hyp[1].nvs" 1920;
	setAttr ".hyp[2].nvs" 1920;
	setAttr ".hyp[3].nvs" 1920;
	setAttr ".anf" yes;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -k on ".an";
	setAttr -k on ".pt";
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultRenderGlobals;
	setAttr ".ep" 1;
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av ".w" 640;
	setAttr -av ".h" 480;
	setAttr -av ".pa";
	setAttr -av ".al";
	setAttr -av ".dar" 1.3333332538604736;
	setAttr -av -k on ".ldar";
	setAttr -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -k on ".isu";
	setAttr -k on ".pdu";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
select -ne :defaultObjectSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off ".eeaa";
	setAttr -k off ".engm";
	setAttr -k off ".mes";
	setAttr -k off ".emb";
	setAttr -av -k off ".mbbf";
	setAttr -k off ".mbs";
	setAttr -k off ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off ".twa";
	setAttr -k off ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :hardwareRenderingGlobals;
	setAttr ".vac" 2;
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av -k on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr ".fn" -type "string" "im";
	setAttr -k on ".if";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -k on ".fir";
	setAttr -k on ".aap";
	setAttr -k on ".gh";
	setAttr -cb on ".sd";
select -ne :hyperGraphLayout;
	setAttr -s 5 ".hyp";
connectAttr "Lucas_Hips.s" "Lucas_LeftUpLeg.is";
connectAttr "Lucas_LeftUpLeg.s" "Lucas_LeftLeg.is";
connectAttr "Lucas_LeftLeg.s" "Lucas_LeftFoot.is";
connectAttr "Lucas_LeftFoot.s" "Lucas_LeftToeBase.is";
connectAttr "Lucas_LeftToeBase.s" "Lucas_LeftFootMiddle1.is";
connectAttr "Lucas_LeftFootMiddle1.s" "Lucas_LeftFootMiddle2.is";
connectAttr "Lucas_Hips.s" "Lucas_RightUpLeg.is";
connectAttr "Lucas_RightUpLeg.s" "Lucas_RightLeg.is";
connectAttr "Lucas_RightLeg.s" "Lucas_RightFoot.is";
connectAttr "Lucas_RightFoot.s" "Lucas_RightToeBase.is";
connectAttr "Lucas_RightToeBase.s" "Lucas_RightFootMiddle1.is";
connectAttr "Lucas_RightFootMiddle1.s" "Lucas_RightFootMiddle2.is";
connectAttr "Lucas_Hips.s" "Lucas_Spine.is";
connectAttr "Lucas_Spine.s" "Lucas_LeftShoulder.is";
connectAttr "Lucas_LeftShoulder.s" "Lucas_LeftArm.is";
connectAttr "Lucas_LeftArm.s" "Lucas_LeftForeArm.is";
connectAttr "Lucas_LeftForeArm.s" "Lucas_LeftHand.is";
connectAttr "Lucas_LeftHand.s" "Lucas_LeftHandThumb1.is";
connectAttr "Lucas_LeftHandThumb1.s" "Lucas_LeftHandThumb2.is";
connectAttr "Lucas_LeftHandThumb2.s" "Lucas_LeftHandThumb3.is";
connectAttr "Lucas_LeftHandThumb3.s" "Lucas_LeftHandThumb4.is";
connectAttr "Lucas_LeftHand.s" "Lucas_LeftHandIndex1.is";
connectAttr "Lucas_LeftHandIndex1.s" "Lucas_LeftHandIndex2.is";
connectAttr "Lucas_LeftHandIndex2.s" "Lucas_LeftHandIndex3.is";
connectAttr "Lucas_LeftHandIndex3.s" "Lucas_LeftHandIndex4.is";
connectAttr "Lucas_LeftHand.s" "Lucas_LeftHandMiddle1.is";
connectAttr "Lucas_LeftHandMiddle1.s" "Lucas_LeftHandMiddle2.is";
connectAttr "Lucas_LeftHandMiddle2.s" "Lucas_LeftHandMiddle3.is";
connectAttr "Lucas_LeftHandMiddle3.s" "Lucas_LeftHandMiddle4.is";
connectAttr "Lucas_LeftHand.s" "Lucas_LeftHandRing1.is";
connectAttr "Lucas_LeftHandRing1.s" "Lucas_LeftHandRing2.is";
connectAttr "Lucas_LeftHandRing2.s" "Lucas_LeftHandRing3.is";
connectAttr "Lucas_LeftHandRing3.s" "Lucas_LeftHandRing4.is";
connectAttr "Lucas_LeftHand.s" "Lucas_LeftHandPinky1.is";
connectAttr "Lucas_LeftHandPinky1.s" "Lucas_LeftHandPinky2.is";
connectAttr "Lucas_LeftHandPinky2.s" "Lucas_LeftHandPinky3.is";
connectAttr "Lucas_LeftHandPinky3.s" "Lucas_LeftHandPinky4.is";
connectAttr "Lucas_Spine.s" "Lucas_RightShoulder.is";
connectAttr "Lucas_RightShoulder.s" "Lucas_RightArm.is";
connectAttr "Lucas_RightArm.s" "Lucas_RightForeArm.is";
connectAttr "Lucas_RightForeArm.s" "Lucas_RightHand.is";
connectAttr "Lucas_RightHand.s" "Lucas_RightHandThumb1.is";
connectAttr "Lucas_RightHandThumb1.s" "Lucas_RightHandThumb2.is";
connectAttr "Lucas_RightHandThumb2.s" "Lucas_RightHandThumb3.is";
connectAttr "Lucas_RightHandThumb3.s" "Lucas_RightHandThumb4.is";
connectAttr "Lucas_RightHand.s" "Lucas_RightHandIndex1.is";
connectAttr "Lucas_RightHandIndex1.s" "Lucas_RightHandIndex2.is";
connectAttr "Lucas_RightHandIndex2.s" "Lucas_RightHandIndex3.is";
connectAttr "Lucas_RightHandIndex3.s" "Lucas_RightHandIndex4.is";
connectAttr "Lucas_RightHand.s" "Lucas_RightHandMiddle1.is";
connectAttr "Lucas_RightHandMiddle1.s" "Lucas_RightHandMiddle2.is";
connectAttr "Lucas_RightHandMiddle2.s" "Lucas_RightHandMiddle3.is";
connectAttr "Lucas_RightHandMiddle3.s" "Lucas_RightHandMiddle4.is";
connectAttr "Lucas_RightHand.s" "Lucas_RightHandRing1.is";
connectAttr "Lucas_RightHandRing1.s" "Lucas_RightHandRing2.is";
connectAttr "Lucas_RightHandRing2.s" "Lucas_RightHandRing3.is";
connectAttr "Lucas_RightHandRing3.s" "Lucas_RightHandRing4.is";
connectAttr "Lucas_RightHand.s" "Lucas_RightHandPinky1.is";
connectAttr "Lucas_RightHandPinky1.s" "Lucas_RightHandPinky2.is";
connectAttr "Lucas_RightHandPinky2.s" "Lucas_RightHandPinky3.is";
connectAttr "Lucas_RightHandPinky3.s" "Lucas_RightHandPinky4.is";
connectAttr "Lucas_Spine.s" "Lucas_Neck.is";
connectAttr "Lucas_Neck.s" "Lucas_Head.is";
connectAttr "V2_defaultLayer.di" "c_eye_ctrl.do";
connectAttr "V2_defaultLayer.di" "l_eye_ctrl.do";
connectAttr "V2_defaultLayer.di" "r_eye_ctrl.do";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "HIKproperties1.msg" "Lucas.propertyState";
connectAttr "HIKSkeletonGeneratorNode1.CharacterNode" "Lucas.SkeletonGenerator";
connectAttr "Lucas_Reference.ch" "Lucas.Reference";
connectAttr "Lucas_Hips.ch" "Lucas.Hips";
connectAttr "Lucas_LeftUpLeg.ch" "Lucas.LeftUpLeg";
connectAttr "Lucas_LeftLeg.ch" "Lucas.LeftLeg";
connectAttr "Lucas_LeftFoot.ch" "Lucas.LeftFoot";
connectAttr "Lucas_RightUpLeg.ch" "Lucas.RightUpLeg";
connectAttr "Lucas_RightLeg.ch" "Lucas.RightLeg";
connectAttr "Lucas_RightFoot.ch" "Lucas.RightFoot";
connectAttr "Lucas_Spine.ch" "Lucas.Spine";
connectAttr "Lucas_LeftArm.ch" "Lucas.LeftArm";
connectAttr "Lucas_LeftForeArm.ch" "Lucas.LeftForeArm";
connectAttr "Lucas_LeftHand.ch" "Lucas.LeftHand";
connectAttr "Lucas_RightArm.ch" "Lucas.RightArm";
connectAttr "Lucas_RightForeArm.ch" "Lucas.RightForeArm";
connectAttr "Lucas_RightHand.ch" "Lucas.RightHand";
connectAttr "Lucas_Head.ch" "Lucas.Head";
connectAttr "Lucas_LeftShoulder.ch" "Lucas.LeftShoulder";
connectAttr "Lucas_RightShoulder.ch" "Lucas.RightShoulder";
connectAttr "Lucas_Neck.ch" "Lucas.Neck";
connectAttr "Lucas_LeftHandThumb1.ch" "Lucas.LeftHandThumb1";
connectAttr "Lucas_LeftHandThumb2.ch" "Lucas.LeftHandThumb2";
connectAttr "Lucas_LeftHandThumb3.ch" "Lucas.LeftHandThumb3";
connectAttr "Lucas_LeftHandThumb4.ch" "Lucas.LeftHandThumb4";
connectAttr "Lucas_LeftHandIndex1.ch" "Lucas.LeftHandIndex1";
connectAttr "Lucas_LeftHandIndex2.ch" "Lucas.LeftHandIndex2";
connectAttr "Lucas_LeftHandIndex3.ch" "Lucas.LeftHandIndex3";
connectAttr "Lucas_LeftHandIndex4.ch" "Lucas.LeftHandIndex4";
connectAttr "Lucas_LeftHandMiddle1.ch" "Lucas.LeftHandMiddle1";
connectAttr "Lucas_LeftHandMiddle2.ch" "Lucas.LeftHandMiddle2";
connectAttr "Lucas_LeftHandMiddle3.ch" "Lucas.LeftHandMiddle3";
connectAttr "Lucas_LeftHandMiddle4.ch" "Lucas.LeftHandMiddle4";
connectAttr "Lucas_LeftHandRing1.ch" "Lucas.LeftHandRing1";
connectAttr "Lucas_LeftHandRing2.ch" "Lucas.LeftHandRing2";
connectAttr "Lucas_LeftHandRing3.ch" "Lucas.LeftHandRing3";
connectAttr "Lucas_LeftHandRing4.ch" "Lucas.LeftHandRing4";
connectAttr "Lucas_LeftHandPinky1.ch" "Lucas.LeftHandPinky1";
connectAttr "Lucas_LeftHandPinky2.ch" "Lucas.LeftHandPinky2";
connectAttr "Lucas_LeftHandPinky3.ch" "Lucas.LeftHandPinky3";
connectAttr "Lucas_LeftHandPinky4.ch" "Lucas.LeftHandPinky4";
connectAttr "Lucas_RightHandThumb1.ch" "Lucas.RightHandThumb1";
connectAttr "Lucas_RightHandThumb2.ch" "Lucas.RightHandThumb2";
connectAttr "Lucas_RightHandThumb3.ch" "Lucas.RightHandThumb3";
connectAttr "Lucas_RightHandThumb4.ch" "Lucas.RightHandThumb4";
connectAttr "Lucas_RightHandIndex1.ch" "Lucas.RightHandIndex1";
connectAttr "Lucas_RightHandIndex2.ch" "Lucas.RightHandIndex2";
connectAttr "Lucas_RightHandIndex3.ch" "Lucas.RightHandIndex3";
connectAttr "Lucas_RightHandIndex4.ch" "Lucas.RightHandIndex4";
connectAttr "Lucas_RightHandMiddle1.ch" "Lucas.RightHandMiddle1";
connectAttr "Lucas_RightHandMiddle2.ch" "Lucas.RightHandMiddle2";
connectAttr "Lucas_RightHandMiddle3.ch" "Lucas.RightHandMiddle3";
connectAttr "Lucas_RightHandMiddle4.ch" "Lucas.RightHandMiddle4";
connectAttr "Lucas_RightHandRing1.ch" "Lucas.RightHandRing1";
connectAttr "Lucas_RightHandRing2.ch" "Lucas.RightHandRing2";
connectAttr "Lucas_RightHandRing3.ch" "Lucas.RightHandRing3";
connectAttr "Lucas_RightHandRing4.ch" "Lucas.RightHandRing4";
connectAttr "Lucas_RightHandPinky1.ch" "Lucas.RightHandPinky1";
connectAttr "Lucas_RightHandPinky2.ch" "Lucas.RightHandPinky2";
connectAttr "Lucas_RightHandPinky3.ch" "Lucas.RightHandPinky3";
connectAttr "Lucas_RightHandPinky4.ch" "Lucas.RightHandPinky4";
connectAttr "Lucas_LeftFootMiddle1.ch" "Lucas.LeftFootMiddle1";
connectAttr "Lucas_LeftFootMiddle2.ch" "Lucas.LeftFootMiddle2";
connectAttr "Lucas_RightFootMiddle1.ch" "Lucas.RightFootMiddle1";
connectAttr "Lucas_RightFootMiddle2.ch" "Lucas.RightFootMiddle2";
connectAttr "Lucas_LeftToeBase.ch" "Lucas.LeftToeBase";
connectAttr "Lucas_RightToeBase.ch" "Lucas.RightToeBase";
connectAttr "HIKproperties1.OutputPropertySetState" "HIKSolverNode1.InputPropertySetState"
		;
connectAttr "Lucas.OutputCharacterDefinition" "HIKSolverNode1.InputCharacterDefinition"
		;
connectAttr "Lucas.OutputCharacterDefinition" "HIKState2SK1.InputCharacterDefinition"
		;
connectAttr "HIKSolverNode1.OutputCharacterState" "HIKState2SK1.InputCharacterState"
		;
connectAttr ":TurtleDefaultBakeLayer.idx" ":TurtleBakeLayerManager.bli[0]";
connectAttr ":TurtleRenderOptions.msg" ":TurtleDefaultBakeLayer.rset";
connectAttr "hyperView1.msg" "nodeEditorPanel1Info.b[0]";
connectAttr "hyperLayout1.msg" "hyperView1.hl";
connectAttr ":TurtleRenderOptions.msg" "hyperLayout1.hyp[0].dn";
connectAttr ":TurtleUIOptions.msg" "hyperLayout1.hyp[1].dn";
connectAttr ":TurtleBakeLayerManager.msg" "hyperLayout1.hyp[2].dn";
connectAttr ":TurtleDefaultBakeLayer.msg" "hyperLayout1.hyp[3].dn";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "c_eye_ctrlShape.msg" ":hyperGraphLayout.hyp[1].dn";
connectAttr "l_eye_ctrlShape.msg" ":hyperGraphLayout.hyp[4].dn";
connectAttr "r_eye_ctrlShape.msg" ":hyperGraphLayout.hyp[5].dn";
connectAttr "l_eye_ctrl.msg" ":hyperGraphLayout.hyp[11].dn";
connectAttr "r_eye_ctrl.msg" ":hyperGraphLayout.hyp[12].dn";
// End of StartRigging.ma
