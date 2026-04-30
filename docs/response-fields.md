# 응답변수 매핑표

이 문서는 붙임3 `지방행정 인허가정보의 제공항목(응답변수) 매핑테이블_20260407수정.xlsx`에서 생성했습니다.
삭제로 표시된 항목은 기본 API 응답 필드가 아니므로 `list_response_fields()`에서는 제외되고, `include_deleted=True`일 때만 반환됩니다.

- 전체 매핑 행: 1011개
- 기본 반환 필드: 848개

| 그룹 | LOCALDATA 영문명 | LOCALDATA 한글명 | 응답변수 | 응답변수 한글명 | 유형 | 길이 | 비고 |
|---|---|---|---|---|---|---:|---|
| 공통제공항목 | `opnSvcId` | 개방서비스ID |  |  |  |  | 삭제 |
| 공통제공항목 | `opnSvcNm` | 개방서비스명 |  |  |  |  | 삭제 |
| 공통제공항목 | `opnSfTeamCode` | 개방자치단체코드 | `OPN_ATMY_GRP_CD` | 개방자치단체코드 | CHAR | 7 |  |
| 공통제공항목 | `mgtNo` | 관리번호 | `MNG_NO` | 관리번호 | VARCHAR2 | 50 |  |
| 공통제공항목 | `updateGbn` | 데이터갱신구분 | `DAT_UPDT_SE` | 데이터갱신구분 | CHAR | 1 |  |
| 공통제공항목 | `updateDt` | 데이터갱신일자 | `DAT_UPDT_PNT` | 데이터갱신시점 | VARCHAR2 | 14 |  |
| 공통제공항목 | `apvPermYmd` | 인허가일자 | `LCPMT_YMD` | 인허가일자 | CHAR | 8 |  |
| 공통제공항목 | `apvCancelYmd` | 인허가취소일자 | `LCPMT_RTRCN_YMD` | 인허가취소일자 | CHAR | 8 |  |
| 공통제공항목 | `trdStateGbn` | 영업상태구분코드 | `SALS_STTS_CD` | 영업상태코드 | VARCHAR2 | 20 |  |
| 공통제공항목 | `trdStateNm` | 영업상태명 | `SALS_STTS_NM` | 영업상태명 | VARCHAR2 | 300 |  |
| 공통제공항목 | `dtlStateGbn` | 상세영업상태코드 | `DTL_SALS_STTS_CD` | 상세영업상태코드 | VARCHAR2 | 4 |  |
| 공통제공항목 | `dtlStateNm` | 상세영업상태명 | `DTL_SALS_STTS_NM` | 상세영업상태명 | VARCHAR2 | 200 |  |
| 공통제공항목 | `dcbYmd` | 폐업일자 | `CLSBIZ_YMD` | 폐업일자 | CHAR | 8 |  |
| 공통제공항목 | `clgStdt` | 휴업시작일자 | `TCBIZ_BGNG_YMD` | 휴업시작일자 | CHAR | 8 |  |
| 공통제공항목 | `clgEnddt` | 휴업종료일자 | `TCBIZ_END_YMD` | 휴업종료일자 | CHAR | 8 |  |
| 공통제공항목 | `ropnYmd` | 재개업일자 | `ROBIZ_YMD` | 재개업일자 | CHAR | 8 |  |
| 공통제공항목 | `siteTel` | 소재지전화번호 | `TELNO` | 소재지전화번호 | VARCHAR2 | 11 |  |
| 공통제공항목 | `siteArea` | 소재지면적 | `LCTN_AREA` | 소재지면적 | VARCHAR2 | 18 |  |
| 공통제공항목 | `sitePostNo` | 소재지우편번호 | `LCTN_ZIP` | 소재지우편번호 | CHAR | 6 |  |
| 공통제공항목 | `siteWhlAddr` | 소재지전체주소 | `LOTNO_ADDR` | 지번주소 | VARCHAR2 | 200 |  |
| 공통제공항목 | `rdnWhlAddr` | 도로명전체주소 | `ROAD_NM_ADDR` | 도로명주소 | VARCHAR2 | 200 |  |
| 공통제공항목 | `rdnPostNo` | 도로명우편번호 | `ROAD_NM_ZIP` | 도로명우편번호 | CHAR | 5 |  |
| 공통제공항목 | `bplcNm` | 사업장명 | `BPLC_NM` | 사업장명 | VARCHAR2 | 200 |  |
| 공통제공항목 | `lastModTs` | 최종수정시점 | `LAST_MDFCN_PNT` | 최종수정시점 | VARCHAR2 | 14 |  |
| 공통제공항목 | `uptaeNm` | 업태구분명 | `BZSTAT_SE_NM` | 업태구분명 | VARCHAR2 | 500 |  |
| 공통제공항목 | `x` | 좌표정보(X) | `CRD_INFO_X` | 좌표X | CHAR | 20 |  |
| 공통제공항목 | `y` | 좌표정보(Y) | `CRD_INFO_Y` | 좌표Y | CHAR | 20 |  |
| 의료기관 | `nurseCnt` | 간호사수 | `NRS_CNT` | 간호사수 | NUMBER | 10 |  |
| 의료기관 | `nursaidCnt` | 간호조무사수 | `NRSAD_CNT` | 간호조무사수 | NUMBER | 13 |  |
| 의료기관 | `bdngLayerCnt` | 건물층수 | `BLDG_FLR_CNT` | 건물층수 | NUMBER | 4 |  |
| 의료기관 | `mgtMbd` | 관리주체 | `MNATH` | 관리주체 | VARCHAR2 | 100 |  |
| 의료기관 | `emerCarGen` | 구급차일반 | `ABLNC_GNRL` | 구급차일반 | NUMBER | 22 |  |
| 의료기관 | `emerCarSpec` | 구급차특수 | `ABLNC_SPCL` | 구급차특수 | NUMBER | 22 |  |
| 의료기관 | `resCnt` | 구조사수 | `MDTECH_CNT` | 구조사수 | VARCHAR2 | 6 |  |
| 의료기관 | `pomFacilAr` | 급식시설면적 | `SCHML_FCLT_AREA` | 급식시설면적 | NUMBER | 13 |  |
| 의료기관 | `etcStfCnt` | 기타인원수 | `ETC_NOPE` | 기타인원수 | NUMBER | 6 |  |
| 의료기관 | `etcEpCnt` | 기타직원수 | `ETC_EMP_CNT` | 기타직원수 | VARCHAR2 | 20 |  |
| 의료기관 | `mmkNurmAr` | 모유수유실면적 | `BRFD_RM_AREA` | 모유수유실면적 | NUMBER | 13 |  |
| 의료기관 | `btRmAr` | 목욕실면적 | `BTH_RM_AREA` | 목욕실면적 | NUMBER | 13 |  |
| 의료기관 | `btpNum` | 미화원수 | `GBGCO_CNT` | 미화원수 | NUMBER | 3 |  |
| 의료기관 | `sicbNum` | 병상수 | `SCKBD_CNT` | 병상수 | NUMBER | 7 |  |
| 의료기관 | `astnEpNum` | 보조직원수 | `ASST_EMP_CNT` | 보조직원수 | NUMBER | 8 |  |
| 의료기관 | `ofeAr` | 사무실면적 | `OFC_AREA` | 사무실면적 | NUMBER | 13 |  |
| 의료기관 | `warmAr` | 세탁실면적 | `WASH_RM_AREA` | 세탁실면적 | NUMBER | 13 |  |
| 의료기관 | `facilMngNum` | 시설관리자수 | `FCLT_MNGR_CNT` | 시설관리자수 | NUMBER | 8 |  |
| 의료기관 | `pharmTrdAr` | 약국영업면적 | `PMCY_SALS_AREA` | 약국영업면적 | NUMBER | 17 |  |
| 의료기관 | `nutrCnt` | 영양사수 | `NUTR_CNT` | 영양사수 | NUMBER | 13 |  |
| 의료기관 | `bbrmAr` | 영유아실면적 | `INFANT_RM_AREA` | 영유아실면적 | NUMBER | 13 |  |
| 의료기관 | `babyRglstNum` | 영유아정원수 | `INFANT_PSCP_CNT` | 영유아정원수 | NUMBER | 5 |  |
| 의료기관 | `mitMdcDepNm` | 완화의료담당부서명 |  |  |  |  | 삭제 |
| 의료기관 | `mitMdcAsgnType` | 완화의료지정형태 |  |  |  |  | 삭제 |
| 의료기관 | `batrAr` | 욕실면적 | `BTHRM_AREA` | 욕실면적 | NUMBER | 13 |  |
| 의료기관 | `metrOrgAssrNm` | 의료기관종별명 | `MDLCR_INST_BTP_NM` | 의료기관종별명 | VARCHAR2 | 200 |  |
| 의료기관 | `metrBosAssrNm` | 의료유사업종별명 | `MDLCR_SMLR_BBTY_NM` | 의료유사업종별명 | VARCHAR2 | 200 |  |
| 의료기관 | `metrpNum` | 의료인수 | `HCWKR_CNT` | 의료인수 | NUMBER | 5 |  |
| 의료기관 | `pgrmAr` | 임산부실면적 | `PRGNW_RM_AREA` | 임산부실면적 | NUMBER | 13 |  |
| 의료기관 | `pwnmRglstNum` | 임산부정원수 | `PRGNW_PSCP_CNT` | 임산부정원수 | NUMBER | 5 |  |
| 의료기관 | `hstrmNum` | 입원실수 | `HSPTLZRM_CNT` | 입원실수 | NUMBER | 5 |  |
| 의료기관 | `qutnOwnerNum` | 자격증소유자수 | `CRTFCT_OWNR_CNT` | 자격증소유자수 | NUMBER | 8 |  |
| 의료기관 | `joriwonToilAr` | 조리원화장실면적 | `CRFCLT_RSTRM_AREA` | 조리원화장실면적 | NUMBER | 13 |  |
| 의료기관 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 의료기관 | `asgnYmd` | 지정일자 | `DSGN_YMD` | 지정일자 | CHAR | 8 |  |
| 의료기관 | `asgnCancelYmd` | 지정취소일자 |  |  |  |  | 삭제 |
| 의료기관 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 의료기관 | `epCnt` | 직원수 | `EMP_CNT` | 직원수 | VARCHAR2 | 20 |  |
| 의료기관 | `medExtrItemsCn` | 진료과목내용 | `MDEXM_SBJCT_CN` | 진료과목내용 | VARCHAR2 | 1000 |  |
| 의료기관 | `medExtrItemsCnNm` | 진료과목내용명 | `MDEXM_SBJCT_CN_NM` | 진료과목내용명 | VARCHAR2 | 2000 |  |
| 의료기관 | `totAr` | 총면적 | `GFA` | 총면적 | NUMBER | 19,9 |  |
| 의료기관 | `totEpNum` | 총인원 |  |  |  |  | 삭제 |
| 의료기관 | `frstAsgnYmd` | 최초지정일자 |  |  |  |  | 삭제 |
| 의료기관 | `copNum` | 취사부수 | `COOK_CNT` | 취사부수 | NUMBER | 3 |  |
| 의료기관 | `storeTrdAr` | 판매점영업면적 | `SLSTR_SALS_AREA` | 판매점영업면적 | NUMBER | 17 |  |
| 의료기관 | `pmtBedNum` | 허가병상수 |  |  |  |  | 삭제 |
| 의료기기 | `heatNum` | 가열기수 | `HTR_CNT` | 가열기수 | NUMBER | 5 |  |
| 의료기기 | `crftUseLessNum` | 기공용레스수 | `FMW_LESS_CNT` | 기공용레스수 | NUMBER | 5 |  |
| 의료기기 | `crftUseMotNum` | 기공용모터수 | `FMW_MTR_CNT` | 기공용모터수 | NUMBER | 5 |  |
| 의료기기 | `crftUseCompreCnt` | 기공용컴프레서수 | `FMW_CMPRSR_CNT` | 기공용컴프레서수 | NUMBER | 5 |  |
| 의료기기 | `sjYn` | 다른 겸업 여부 | `OTR_SDJB_YN` | 다른겸업여부 | VARCHAR2 | 1 |  |
| 의료기기 | `pupilDistMeasNum` | 동공거리측정기수 | `PPL_DSTNC_MEINS_CNT` | 동공거리측정기수 | NUMBER | 5 |  |
| 의료기기 | `lensCutNum` | 렌즈절단기수 | `LNS_CTTMCHN_CNT` | 렌즈절단기수 | NUMBER | 5 |  |
| 의료기기 | `sbmCnt` | 샌드기수 | `SNDER_CNT` | 샌드기수 | NUMBER | 5 |  |
| 의료기기 | `suvyNum` | 서베이어수 | `SVYR_CNT` | 서베이어수 | NUMBER | 5 |  |
| 의료기기 | `medKind` | 수리대상 의료기기의 유형 | `RPR_TRGT_MDLCR_ISTR_OF_TYPE` | 수리대상의료기기의유형 | VARCHAR2 | 200 |  |
| 의료기기 | `eyePyoNum` | 시력표수 | `EYCHRT_CNT` | 시력표수 | NUMBER | 5 |  |
| 의료기기 | `acetNum` | 아세틸렌수 | `ACTYL_CNT` | 아세틸렌수 | NUMBER | 5 |  |
| 의료기기 | `glsWasherNum` | 안경세척기수 | `GLSSS_WASHMCHN_CNT` | 안경세척기수 | NUMBER | 5 |  |
| 의료기기 | `trdScp` | 영업규모 |  |  |  |  | 삭제 |
| 의료기기 | `ctplCtmceNum` | 원심주조기수 | `CNTFGL_CSTMCHN_CNT` | 원심주조기수 | NUMBER | 5 |  |
| 의료기기 | `efurNum` | 전기로수 | `PRVTM_BY_CNT` | 전기로수 | NUMBER | 5 |  |
| 의료기기 | `defptRfrtGgNum` | 정점굴절계기수 | `VRTX_RFRCTMTR_CNT` | 정점굴절계기수 | NUMBER | 5 |  |
| 의료기기 | `pptnUseGrndNum` | 조제용연마기수 | `DSPNS_POLMCHN_CNT` | 조제용연마기수 | NUMBER | 5 |  |
| 의료기기 | `buryCnt` | 진공매몰기수 | `VAC_INVTMCHN_CNT` | 진공매몰기수 | NUMBER | 5 |  |
| 의료기기 | `vitrNum` | 진동기수 | `VBRTR_CNT` | 진동기수 | NUMBER | 5 |  |
| 의료기기 | `spwvClerNum` | 초음파청소기수 | `ULSD_VACCLR_CNT` | 초음파청소기수 | NUMBER | 5 |  |
| 의료기기 | `totScp` | 총규모 | `TOTAL_SCL` | 총규모 | VARCHAR2 | 4000 |  |
| 의료기기 | `totAr` | 총면적 | `GFA` | 총면적 | NUMBER | 19,9 |  |
| 의료기기 | `msmChairNum` | 측정의자수 | `MSRMT_CHAI_CNT` | 측정의자수 | NUMBER | 5 |  |
| 의료기기 | `dentiUsePressNum` | 치과용프레스수 | `DNTLU_PRSMCHN_CNT` | 치과용프레스수 | NUMBER | 5 |  |
| 의료기기 | `trmNum` | 트리머수 | `TRMR_CNT` | 트리머수 | NUMBER | 5 |  |
| 의료기기 | `pcanNum` | 포셀린로수 | `PRCLNFNC_CNT` | 포셀린로수 | NUMBER | 5 |  |
| 의료기기 | `sampLensNum` | 표본렌즈수 | `SMPLLNS_CNT` | 표본렌즈수 | NUMBER | 5 |  |
| 의료기기 | `pindexCnt` | 핀덱스수 | `PNDX_CNT` | 핀덱스수 | NUMBER | 5 |  |
| 동물 | `rgtMbdSno` | 권리주체일련번호 | `RGHT_MNBD_SN` | 권리주체일련번호 | VARCHAR2 | 3 |  |
| 동물 | `lindPrcbGbnNm` | 상세업무구분명 | `DTL_TASK_SE_NM` | 상세업무구분명 | VARCHAR2 | 500 |  |
| 동물 | `lindJobGbnNm` | 업무구분명 |  |  |  |  | 삭제 |
| 동물 | `totEpNum` | 총직원수 |  |  |  |  | 삭제 |
| 축산 | `rgtMbdSno` | 권리주체일련번호 | `RGHT_MNBD_SN` | 권리주체일련번호 | VARCHAR2 | 3 |  |
| 축산 | `cfrmGbnCtn` | 주사육업종 | `PRMN_LSFBIZ_SPECS` | 주사육업종 | VARCHAR2 | 100 |  |
| 축산 | `totEpNum` | 총직원수 | `TNOEMP` | 총직원수 | VARCHAR2 | 20 |  |
| 축산 | `lindPrcbGbnNm` | 축산물가공업구분명 | `LSPRD_PRCSNBIZ_SE_NM` | 축산물가공업구분명 | VARCHAR2 | 500 |  |
| 축산 | `lindJobGbnNm` | 축산업무구분명 | `ANMLHSBNDR_TASK_SE_NM` | 축산업무구분명 | VARCHAR2 | 200 |  |
| 축산 | `lindSeqNo` | 축산일련번호 | `ANMLHSBNDR_SN` | 축산일련번호 | NUMBER | 9 |  |
| 게임 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 게임 | `perplaFormSeNm` | 공연장형태구분명 |  |  |  |  | 삭제 |
| 게임 | `bfGameOcptEctCobNm` | 기존게임업외업종명 | `EXS_GAMBIZ_ADDT_TPBIZ_NM` | 기존게임업외업종명 | VARCHAR2 | 200 |  |
| 게임 | `noroomCnt` | 노래방실수 | `KAROOM_RM_CNT` | 노래방실수 | NUMBER | 3 |  |
| 게임 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 게임 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 게임 | `souarFacilYn` | 방음시설여부 | `SNDPRF_FCLT_YN` | 방음시설여부 | VARCHAR2 | 1 |  |
| 게임 | `vdoRetorNm` | 비디오재생기명 | `VIDEO_PLYR_NM` | 비디오재생기명 | VARCHAR2 | 200 |  |
| 게임 | `emerStairYn` | 비상계단여부 | `EMSTC_YN` | 비상계단여부 | VARCHAR2 | 1 |  |
| 게임 | `emexYn` | 비상구여부 | `EMEXIT_YN` | 비상구여부 | VARCHAR2 | 1 |  |
| 게임 | `fireFacilYn` | 소방시설여부 | `FRFGT_FCLT_YN` | 소방시설여부 | VARCHAR2 | 1 |  |
| 게임 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 게임 | `soundFacilYn` | 음향시설여부 | `SOND_FCLT_YN` | 음향시설여부 | VARCHAR2 | 1 |  |
| 게임 | `autoChaairYn` | 자동환기여부 | `AUTO_VNTLTN_YN` | 자동환기여부 | VARCHAR2 | 1 |  |
| 게임 | `prvdGathinNm` | 제공게임물명 | `PVSN_VG_NM` | 제공게임물명 | VARCHAR2 | 200 |  |
| 게임 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 게임 | `lghtFacilYn` | 조명시설유무 | `LTG_FCLT_EN` | 조명시설유무 | VARCHAR2 | 1 |  |
| 게임 | `lghtFacilInillu` | 조명시설조도 | `LTG_FCLT_ILLMNT` | 조명시설조도 | NUMBER | 13 |  |
| 게임 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 게임 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 게임 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 게임 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 게임 | `bgroomCnt` | 청소년실수 | `JVNILE_RM_CNT` | 청소년실수 | NUMBER | 3 |  |
| 게임 | `bgroomYn` | 청소년실여부 | `JVNILE_RM_YN` | 청소년실여부 | VARCHAR2 | 1 |  |
| 게임 | `totGasysCnt` | 총게임기수 | `TOTAL_GMCON_CNT` | 총게임기수 | NUMBER | 3 |  |
| 게임 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 게임 | `frstRegTs` | 최초등록시점 |  |  |  |  | 삭제 |
| 게임 | `pasgBreth` | 통로너비 | `PASSG_WIDTH` | 통로너비 | NUMBER | 13 |  |
| 게임 | `specLghtYn` | 특수조명여부 | `SPCL_LTG_YN` | 특수조명여부 | VARCHAR2 | 1 |  |
| 게임 | `cnveFacilYn` | 편의시설여부 | `CVNFCL_YN` | 편의시설여부 | CHAR | 1 |  |
| 게임 | `actlNm` | 품목명 |  |  |  |  | 삭제 |
| 게임 | `etcDtl2` | 기타내역2 | `ETC_DSCTN_2` | 기타내역2 | VARCHAR2 | 1000 |  |
| 공연 | `stroomCnt` | 객실수 | `GSRM_CNT` | 객실수 | NUMBER | 10 |  |
| 공연 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 공연 | `cnstYarea` | 건축연면적 | `ARCH_TFA` | 건축연면적 | NUMBER | 18 |  |
| 공연 | `svnSr` | 기념품종류 | `SVNR_KND` | 기념품종류 | VARCHAR2 | 100 |  |
| 공연 | `plnInsurStdt` | 기획여행보험시작일자 |  |  |  |  | 삭제 |
| 공연 | `plnInsurEnddt` | 기획여행보험종료일자 |  |  |  |  | 삭제 |
| 공연 | `playUtsCntDtl` | 놀이기구수내역 |  |  |  |  | 삭제 |
| 공연 | `playFacilCnt` | 놀이시설수 |  |  |  |  | 삭제 |
| 공연 | `stageAr` | 무대면적 | `STAGE_AREA` | 무대면적 | NUMBER | 13 |  |
| 공연 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 공연 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 공연 | `geicpFacilEn` | 발전시설유무 |  |  |  |  | 삭제 |
| 공연 | `bcFacilEn` | 방송시설유무 |  |  |  |  | 삭제 |
| 공연 | `insurOrgNm` | 보험기관명 | `INSRNC_INST_NM` | 보험기관명 | VARCHAR2 | 200 |  |
| 공연 | `insurStdt` | 보험시작일자 | `INSRNC_BGNG_YMD` | 보험시작일자 | CHAR | 8 |  |
| 공연 | `insurEnddt` | 보험종료일자 | `INSRNC_END_YMD` | 보험종료일자 | CHAR | 8 |  |
| 공연 | `afc` | 부대시설내역 |  |  |  |  | 삭제 |
| 공연 | `shpInfo` | 선박제원 | `VSL_SPEC` | 선박제원 | VARCHAR2 | 100 |  |
| 공연 | `shpCnt` | 선박척수 | `VSL_SCNT_CNT` | 선박척수 | NUMBER | 1 |  |
| 공연 | `shpTotTons` | 선박총톤수 | `VSL_TOTAL_TON` | 선박총톤수 | NUMBER | 13 |  |
| 공연 | `facilScp` | 시설규모 | `FCLT_SCL` | 시설규모 | NUMBER | 9 |  |
| 공연 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 공연 | `infobEn` | 안내소유무 |  |  |  |  | 삭제 |
| 공연 | `engStnTrnmNm` | 영문상호명 | `ENG_CONM_NM` | 영문상호명 | VARCHAR2 | 100 |  |
| 공연 | `engStnTrnmAddr` | 영문상호주소 | `ENG_CONM_ADDR` | 영문상호주소 | VARCHAR2 | 300 |  |
| 공연 | `dispenEn` | 의무실유무 |  |  |  |  | 삭제 |
| 공연 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 공연 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 공연 | `chairCnt` | 좌석수 | `SEAT_CNT` | 좌석수 | NUMBER | 14 |  |
| 공연 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 공연 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 공연 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 공연 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 공연 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 공연 | `meetSamTimeSygStf` | 회의실별동시수용인원 | `CFRM_PER_CNCR_ACTC_PERNE` | 회의실별동시수용인원 | NUMBER | 10 |  |
| 관광 | `openYmd` | 개관일자 | `OPNNG_YMD` | 개관일자 | CHAR | 8 |  |
| 관광 | `stroomCnt` | 객실수 | `GSRM_CNT` | 객실수 | NUMBER | 10 |  |
| 관광 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 관광 | `cnstYarea` | 건축연면적 | `ARCH_TFA` | 건축연면적 | NUMBER | 18 |  |
| 관광 | `svnSr` | 기념품종류 | `SVNR_KND` | 기념품종류 | VARCHAR2 | 100 |  |
| 관광 | `plnInsurStdt` | 기획여행보험시작일자 | `PLNNG_TRVL_INSRNC_BGNG_YMD` | 기획여행보험시작일자 | VARCHAR2 | 8 |  |
| 관광 | `plnInsurEnddt` | 기획여행보험종료일자 | `PLNNG_TRVL_INSRNC_END_YMD` | 기획여행보험종료일자 | VARCHAR2 | 8 |  |
| 관광 | `playUtsCntDtl` | 놀이기구수내역 | `AMRIDE_CNT_DSCTN` | 놀이기구수내역 | VARCHAR2 | 250 |  |
| 관광 | `playFacilCnt` | 놀이시설수 | `PLAY_FCLT_CNT` | 놀이시설수 | NUMBER | 4 |  |
| 관광 | `stageAr` | 무대면적 | `STAGE_AREA` | 무대면적 | NUMBER | 13 |  |
| 관광 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 관광 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 관광 | `museumKindNm` | 박물관미술관유형명 | `MSM_ARTM_TYPE_NM` | 박물관미술관유형명 | VARCHAR2 | 200 |  |
| 관광 | `museumSortNm` | 박물관미술관종류명 | `MSM_ARTM_KND_NM` | 박물관미술관종류명 | VARCHAR2 | 200 |  |
| 관광 | `geicpFacilEn` | 발전시설유무 | `DEV_FCLT_EN` | 발전시설유무 | VARCHAR2 | 1 |  |
| 관광 | `bcFacilEn` | 방송시설유무 | `BRDC_FCLT_EN` | 방송시설유무 | VARCHAR2 | 1 |  |
| 관광 | `bupNm` | 법인명 | `CORP_NM` | 법인명 | VARCHAR2 | 100 |  |
| 관광 | `bupEsbmntObj` | 법인설립목적 | `CORP_FNDN_PRPS` | 법인설립목적 | VARCHAR2 | 500 |  |
| 관광 | `bupDisorgYmd` | 법인해산일자 | `CORP_DSBND_YMD` | 법인해산일자 | VARCHAR2 | 8 |  |
| 관광 | `insurOrgNm` | 보험기관명 | `INSRNC_INST_NM` | 보험기관명 | VARCHAR2 | 200 |  |
| 관광 | `insurStdt` | 보험시작일자 | `INSRNC_BGNG_YMD` | 보험시작일자 | CHAR | 8 |  |
| 관광 | `insurEnddt` | 보험종료일자 | `INSRNC_END_YMD` | 보험종료일자 | CHAR | 8 |  |
| 관광 | `afc` | 부대시설내역 | `SBSD_FCLT_DSCTN` | 부대시설내역 | VARCHAR2 | 250 |  |
| 관광 | `shpInfo` | 선박제원 | `VSL_SPEC` | 선박제원 | VARCHAR2 | 100 |  |
| 관광 | `shpCnt` | 선박척수 | `VSL_SCNT_CNT` | 선박척수 | NUMBER | 1 |  |
| 관광 | `shpTotTons` | 선박총톤수 | `VSL_TOTAL_TON` | 선박총톤수 | NUMBER | 13 |  |
| 관광 | `mngMbdNm` | 설립_운영주체구분명 | `FNDN_OPER_MNBD_SE_NM` | 설립운영주체구분명 | VARCHAR2 | 200 |  |
| 관광 | `ndLoan` | 소요자금 | `REQ_FNDS` | 소요자금 | VARCHAR2 | 20 |  |
| 관광 | `monkNum` | 승려수 | `MNK_CNT` | 승려수 | NUMBER | 5 |  |
| 관광 | `facilScp` | 시설규모 | `FCLT_SCL` | 시설규모 | NUMBER | 9 |  |
| 관광 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 관광 | `belvNum` | 신도수 | `BLVR_CNT` | 신도수 | NUMBER | 5 |  |
| 관광 | `infobEn` | 안내소유무 | `INDSK_EN` | 안내소유무 | VARCHAR2 | 1 |  |
| 관광 | `engStnTrnmNm` | 영문상호명 | `ENG_CONM_NM` | 영문상호명 | VARCHAR2 | 100 |  |
| 관광 | `engStnTrnmAddr` | 영문상호주소 | `ENG_CONM_ADDR` | 영문상호주소 | VARCHAR2 | 300 |  |
| 관광 | `originHist` | 유래연혁 | `ORIG_CRNCL` | 유래연혁 | VARCHAR2 | 4000 |  |
| 관광 | `dispenEn` | 의무실유무 | `INFIRM_EN` | 의무실유무 | VARCHAR2 | 1 |  |
| 관광 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 관광 | `tdtpNm` | 전통사찰명 | `TRDTN_TMPL_NM` | 전통사찰명 | VARCHAR2 | 200 |  |
| 관광 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 관광 | `chairCnt` | 좌석수 | `SEAT_CNT` | 좌석수 | NUMBER | 14 |  |
| 관광 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 관광 | `jgongYmd` | 준공일자 | `CMCN_YMD` | 준공일자 | CHAR | 8 |  |
| 관광 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 관광 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 관광 | `asgnCancel` | 지정취소 | `DSGN_RTRCN` | 지정취소 | VARCHAR2 | 1 |  |
| 관광 | `asgnCancelWhy` | 지정취소사유 | `DSGN_RTRCN_RSN` | 지정취소사유 | VARCHAR2 | 4000 |  |
| 관광 | `asgnCancelYmd` | 지정취소일자 | `DSGN_RTRCN_YMD` | 지정취소일자 | CHAR | 8 |  |
| 관광 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 관광 | `estbHdate` | 창립연대 | `FONDG_SLDT` | 창립연대 | VARCHAR2 | 100 |  |
| 관광 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 관광 | `closeWhy` | 폐관사유 | `CLDH_RSN` | 폐관사유 | VARCHAR2 | 200 |  |
| 관광 | `closeYmd` | 폐관일자 | `CLDH_YMD` | 폐관일자 | VARCHAR2 | 8 |  |
| 관광 | `permCn` | 허가조건 | `PRMSN_CND` | 허가조건 | VARCHAR2 | 2000 |  |
| 관광 | `meetSamTimeSygStf` | 회의실별동시수용인원 | `CFRM_PER_CNCR_ACTC_PERNE` | 회의실별동시수용인원 | NUMBER | 10 |  |
| 문화기획 | `openYmd` | 개관일자 |  |  |  |  | 삭제 |
| 문화기획 | `stroomCnt` | 객실수 | `GSRM_CNT` | 객실수 | NUMBER | 10 |  |
| 문화기획 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 문화기획 | `cnstYarea` | 건축연면적 | `ARCH_TFA` | 건축연면적 | NUMBER | 18 |  |
| 문화기획 | `perplaFormSeNm` | 공연장형태구분명 |  |  |  |  | 삭제 |
| 문화기획 | `svnSr` | 기념품종류 | `SVNR_KND` | 기념품종류 | VARCHAR2 | 100 |  |
| 문화기획 | `bfGameOcptEctCobNm` | 기존게임업외업종명 |  |  |  |  | 삭제 |
| 문화기획 | `plnInsurStdt` | 기획여행보험시작일자 |  |  |  |  | 삭제 |
| 문화기획 | `plnInsurEnddt` | 기획여행보험종료일자 |  |  |  |  | 삭제 |
| 문화기획 | `noroomCnt` | 노래방실수 |  |  |  |  | 삭제 |
| 문화기획 | `playUtsCntDtl` | 놀이기구수내역 |  |  |  |  | 삭제 |
| 문화기획 | `playFacilCnt` | 놀이시설수 |  |  |  |  | 삭제 |
| 문화기획 | `stageAr` | 무대면적 | `STAGE_AREA` | 무대면적 | NUMBER | 13 |  |
| 문화기획 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 문화기획 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 문화기획 | `museumKindNm` | 박물관미술관유형명 |  |  |  |  | 삭제 |
| 문화기획 | `museumSortNm` | 박물관미술관종류명 |  |  |  |  | 삭제 |
| 문화기획 | `geicpFacilEn` | 발전시설유무 |  |  |  |  | 삭제 |
| 문화기획 | `bcFacilEn` | 방송시설유무 |  |  |  |  | 삭제 |
| 문화기획 | `souarFacilYn` | 방음시설여부 |  |  |  |  | 삭제 |
| 문화기획 | `bupNm` | 법인명 | `CORP_NM` | 법인명 | VARCHAR2 | 100 |  |
| 문화기획 | `bupEsbmntObj` | 법인설립목적 | `CORP_FNDN_PRPS` | 법인설립목적 | VARCHAR2 | 500 |  |
| 문화기획 | `bupDisorgYmd` | 법인해산일자 | `CORP_DSBND_YMD` | 법인해산일자 | VARCHAR2 | 8 |  |
| 문화기획 | `insurOrgNm` | 보험기관명 | `INSRNC_INST_NM` | 보험기관명 | VARCHAR2 | 200 |  |
| 문화기획 | `insurStdt` | 보험시작일자 | `INSRNC_BGNG_YMD` | 보험시작일자 | CHAR | 8 |  |
| 문화기획 | `insurEnddt` | 보험종료일자 | `INSRNC_END_YMD` | 보험종료일자 | CHAR | 8 |  |
| 문화기획 | `afc` | 부대시설내역 |  |  |  |  | 삭제 |
| 문화기획 | `vdoRetorNm` | 비디오재생기명 |  |  |  |  | 삭제 |
| 문화기획 | `emerStairYn` | 비상계단여부 |  |  |  |  | 삭제 |
| 문화기획 | `emexYn` | 비상구여부 |  |  |  |  | 삭제 |
| 문화기획 | `shpInfo` | 선박제원 | `VSL_SPEC` | 선박제원 | VARCHAR2 | 100 |  |
| 문화기획 | `shpCnt` | 선박척수 | `VSL_SCNT_CNT` | 선박척수 | NUMBER | 1 |  |
| 문화기획 | `shpTotTons` | 선박총톤수 | `VSL_TOTAL_TON` | 선박총톤수 | NUMBER | 13 |  |
| 문화기획 | `mngMbdNm` | 설립_운영주체구분명 |  |  |  |  | 삭제 |
| 문화기획 | `fireFacilYn` | 소방시설여부 |  |  |  |  | 삭제 |
| 문화기획 | `ndLoan` | 소요자금 |  |  |  |  | 삭제 |
| 문화기획 | `facilScp` | 시설규모 | `FCLT_SCL` | 시설규모 | NUMBER | 9 |  |
| 문화기획 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 문화기획 | `infobEn` | 안내소유무 |  |  |  |  | 삭제 |
| 문화기획 | `engStnTrnmNm` | 영문상호명 | `ENG_CONM_NM` | 영문상호명 | VARCHAR2 | 100 |  |
| 문화기획 | `engStnTrnmAddr` | 영문상호주소 | `ENG_CONM_ADDR` | 영문상호주소 | VARCHAR2 | 300 |  |
| 문화기획 | `soundFacilYn` | 음향시설여부 |  |  |  |  | 삭제 |
| 문화기획 | `dispenEn` | 의무실유무 |  |  |  |  | 삭제 |
| 문화기획 | `autoChaairYn` | 자동환기여부 |  |  |  |  | 삭제 |
| 문화기획 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 문화기획 | `prvdGathinNm` | 제공게임물명 |  |  |  |  | 삭제 |
| 문화기획 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 문화기획 | `lghtFacilYn` | 조명시설유무 |  |  |  |  | 삭제 |
| 문화기획 | `lghtFacilInillu` | 조명시설조도 |  |  |  |  | 삭제 |
| 문화기획 | `chairCnt` | 좌석수 | `SEAT_CNT` | 좌석수 | NUMBER | 14 |  |
| 문화기획 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 문화기획 | `jgongYmd` | 준공일자 |  |  |  |  | 삭제 |
| 문화기획 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 문화기획 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 문화기획 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 문화기획 | `bgroomCnt` | 청소년실수 |  |  |  |  | 삭제 |
| 문화기획 | `bgroomYn` | 청소년실여부 |  |  |  |  | 삭제 |
| 문화기획 | `totGasysCnt` | 총게임기수 |  |  |  |  | 삭제 |
| 문화기획 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 문화기획 | `frstRegTs` | 최초등록시점 |  |  |  |  | 삭제 |
| 문화기획 | `pasgBreth` | 통로너비 |  |  |  |  | 삭제 |
| 문화기획 | `specLghtYn` | 특수조명여부 |  |  |  |  | 삭제 |
| 문화기획 | `cnveFacilYn` | 편의시설여부 |  |  |  |  | 삭제 |
| 문화기획 | `closeWhy` | 폐관사유 |  |  |  |  | 삭제 |
| 문화기획 | `closeYmd` | 폐관일자 |  |  |  |  | 삭제 |
| 문화기획 | `actlNm` | 품목명 | `ITEM_NM` | 품목명 | VARCHAR2 | 200 |  |
| 문화기획 | `permCn` | 허가조건 | `PRMSN_CND` | 허가조건 | VARCHAR2 | 2000 |  |
| 문화기획 | `meetSamTimeSygStf` | 회의실별동시수용인원 | `CFRM_PER_CNCR_ACTC_PERNE` | 회의실별동시수용인원 | NUMBER | 10 |  |
| 노래방 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 노래방 | `perplaFormSeNm` | 공연장형태구분명 |  |  |  |  | 삭제 |
| 노래방 | `bfGameOcptEctCobNm` | 기존게임업외업종명 | `EXS_GAMBIZ_ADDT_TPBIZ_NM` | 기존게임업외업종명 | VARCHAR2 | 200 |  |
| 노래방 | `noroomCnt` | 노래방실수 | `KAROOM_RM_CNT` | 노래방실수 | NUMBER | 3 |  |
| 노래방 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 노래방 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 노래방 | `souarFacilYn` | 방음시설여부 | `SNDPRF_FCLT_YN` | 방음시설여부 | VARCHAR2 | 1 |  |
| 노래방 | `vdoRetorNm` | 비디오재생기명 | `VIDEO_PLYR_NM` | 비디오재생기명 | VARCHAR2 | 200 |  |
| 노래방 | `emerStairYn` | 비상계단여부 | `EMSTC_YN` | 비상계단여부 | VARCHAR2 | 1 |  |
| 노래방 | `emexYn` | 비상구여부 | `EMEXIT_YN` | 비상구여부 | VARCHAR2 | 1 |  |
| 노래방 | `fireFacilYn` | 소방시설여부 | `FRFGT_FCLT_YN` | 소방시설여부 | VARCHAR2 | 1 |  |
| 노래방 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 노래방 | `soundFacilYn` | 음향시설여부 | `SOND_FCLT_YN` | 음향시설여부 | VARCHAR2 | 1 |  |
| 노래방 | `autoChaairYn` | 자동환기여부 | `AUTO_VNTLTN_YN` | 자동환기여부 | VARCHAR2 | 1 |  |
| 노래방 | `prvdGathinNm` | 제공게임물명 | `PVSN_VG_NM` | 제공게임물명 | VARCHAR2 | 200 |  |
| 노래방 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 노래방 | `lghtFacilYn` | 조명시설유무 | `LTG_FCLT_EN` | 조명시설유무 | VARCHAR2 | 1 |  |
| 노래방 | `lghtFacilInillu` | 조명시설조도 | `LTG_FCLT_ILLMNT` | 조명시설조도 | NUMBER | 13 |  |
| 노래방 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 노래방 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 노래방 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 노래방 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 노래방 | `bgroomCnt` | 청소년실수 | `JVNILE_RM_CNT` | 청소년실수 | NUMBER | 3 |  |
| 노래방 | `bgroomYn` | 청소년실여부 | `JVNILE_RM_YN` | 청소년실여부 | VARCHAR2 | 1 |  |
| 노래방 | `totGasysCnt` | 총게임기수 | `TOTAL_GMCON_CNT` | 총게임기수 | NUMBER | 3 |  |
| 노래방 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 노래방 | `frstRegTs` | 최초등록시점 |  |  |  |  | 삭제 |
| 노래방 | `pasgBreth` | 통로너비 | `PASSG_WIDTH` | 통로너비 | NUMBER | 13 |  |
| 노래방 | `specLghtYn` | 특수조명여부 | `SPCL_LTG_YN` | 특수조명여부 | VARCHAR2 | 1 |  |
| 노래방 | `cnveFacilYn` | 편의시설여부 | `CVNFCL_YN` | 편의시설여부 | CHAR | 1 |  |
| 노래방 | `actlNm` | 품목명 |  |  |  |  | 삭제 |
| 비디오 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 비디오 | `perplaFormSeNm` | 공연장형태구분명 |  |  |  |  | 삭제 |
| 비디오 | `bfGameOcptEctCobNm` | 기존게임업외업종명 | `EXS_GAMBIZ_ADDT_TPBIZ_NM` | 기존게임업외업종명 | VARCHAR2 | 200 |  |
| 비디오 | `noroomCnt` | 노래방실수 | `KAROOM_RM_CNT` | 노래방실수 | NUMBER | 3 |  |
| 비디오 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 비디오 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 비디오 | `souarFacilYn` | 방음시설여부 | `SNDPRF_FCLT_YN` | 방음시설여부 | VARCHAR2 | 1 |  |
| 비디오 | `vdoRetorNm` | 비디오재생기명 | `VIDEO_PLYR_NM` | 비디오재생기명 | VARCHAR2 | 200 |  |
| 비디오 | `emerStairYn` | 비상계단여부 | `EMSTC_YN` | 비상계단여부 | VARCHAR2 | 1 |  |
| 비디오 | `emexYn` | 비상구여부 | `EMEXIT_YN` | 비상구여부 | VARCHAR2 | 1 |  |
| 비디오 | `fireFacilYn` | 소방시설여부 | `FRFGT_FCLT_YN` | 소방시설여부 | VARCHAR2 | 1 |  |
| 비디오 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 비디오 | `soundFacilYn` | 음향시설여부 | `SOND_FCLT_YN` | 음향시설여부 | VARCHAR2 | 1 |  |
| 비디오 | `autoChaairYn` | 자동환기여부 | `AUTO_VNTLTN_YN` | 자동환기여부 | VARCHAR2 | 1 |  |
| 비디오 | `prvdGathinNm` | 제공게임물명 | `PVSN_VG_NM` | 제공게임물명 | VARCHAR2 | 200 |  |
| 비디오 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 비디오 | `lghtFacilYn` | 조명시설유무 | `LTG_FCLT_EN` | 조명시설유무 | VARCHAR2 | 1 |  |
| 비디오 | `lghtFacilInillu` | 조명시설조도 | `LTG_FCLT_ILLMNT` | 조명시설조도 | NUMBER | 13 |  |
| 비디오 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 비디오 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 비디오 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 비디오 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 비디오 | `bgroomCnt` | 청소년실수 | `JVNILE_RM_CNT` | 청소년실수 | NUMBER | 3 |  |
| 비디오 | `bgroomYn` | 청소년실여부 | `JVNILE_RM_YN` | 청소년실여부 | VARCHAR2 | 1 |  |
| 비디오 | `totGasysCnt` | 총게임기수 | `TOTAL_GMCON_CNT` | 총게임기수 | NUMBER | 3 |  |
| 비디오 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 비디오 | `frstRegTs` | 최초등록시점 |  |  |  |  | 삭제 |
| 비디오 | `pasgBreth` | 통로너비 | `PASSG_WIDTH` | 통로너비 | NUMBER | 13 |  |
| 비디오 | `specLghtYn` | 특수조명여부 | `SPCL_LTG_YN` | 특수조명여부 | VARCHAR2 | 1 |  |
| 비디오 | `cnveFacilYn` | 편의시설여부 | `CVNFCL_YN` | 편의시설여부 | CHAR | 1 |  |
| 비디오 | `actlNm` | 품목명 |  |  |  |  | 삭제 |
| 숙박 | `stroomCnt` | 객실수 | `GSRM_CNT` | 객실수 | NUMBER | 10 |  |
| 숙박 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 숙박 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 숙박 | `bdngJisgFlrCnt` | 건물지상층수 | `BLDG_GRND_FLR_CNT` | 건물지상층수 | NUMBER | 3 |  |
| 숙박 | `bdngUnderFlrCnt` | 건물지하층수 | `BLDG_UDGD_FLR_CNT` | 건물지하층수 | NUMBER | 3 |  |
| 숙박 | `cnstYarea` | 건축연면적 | `ARCH_TFA` | 건축연면적 | NUMBER | 18 |  |
| 숙박 | `svnSr` | 기념품종류 | `SVNR_KND` | 기념품종류 | VARCHAR2 | 100 |  |
| 숙박 | `plnInsurStdt` | 기획여행보험시작일자 |  |  |  |  | 삭제 |
| 숙박 | `plnInsurEnddt` | 기획여행보험종료일자 |  |  |  |  | 삭제 |
| 숙박 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 숙박 | `playUtsCntDtl` | 놀이기구수내역 |  |  |  |  | 삭제 |
| 숙박 | `playFacilCnt` | 놀이시설수 |  |  |  |  | 삭제 |
| 숙박 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 숙박 | `stageAr` | 무대면적 | `STAGE_AREA` | 무대면적 | NUMBER | 13 |  |
| 숙박 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 숙박 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 숙박 | `geicpFacilEn` | 발전시설유무 |  |  |  |  | 삭제 |
| 숙박 | `bcFacilEn` | 방송시설유무 |  |  |  |  | 삭제 |
| 숙박 | `insurOrgNm` | 보험기관명 | `INSRNC_INST_NM` | 보험기관명 | VARCHAR2 | 200 |  |
| 숙박 | `insurStdt` | 보험시작일자 | `INSRNC_BGNG_YMD` | 보험시작일자 | CHAR | 8 |  |
| 숙박 | `insurEnddt` | 보험종료일자 | `INSRNC_END_YMD` | 보험종료일자 | CHAR | 8 |  |
| 숙박 | `afc` | 부대시설내역 |  |  |  |  | 삭제 |
| 숙박 | `useJisgEndFlr` | 사용끝지상층 | `USE_ED_GRND_FLR` | 사용끝지상층 | NUMBER | 3 |  |
| 숙박 | `useUnderEndFlr` | 사용끝지하층 | `USE_ED_UDGD_FLR` | 사용끝지하층 | NUMBER | 3 |  |
| 숙박 | `useJisgStFlr` | 사용시작지상층 | `USE_BGNG_GRND_FLR` | 사용시작지상층 | NUMBER | 3 |  |
| 숙박 | `useUnderStFlr` | 사용시작지하층 | `USE_BGNG_UDGD_FLR` | 사용시작지하층 | NUMBER | 3 |  |
| 숙박 | `shpInfo` | 선박제원 | `VSL_SPEC` | 선박제원 | VARCHAR2 | 100 |  |
| 숙박 | `shpCnt` | 선박척수 | `VSL_SCNT_CNT` | 선박척수 | NUMBER | 1 |  |
| 숙박 | `shpTotTons` | 선박총톤수 | `VSL_TOTAL_TON` | 선박총톤수 | NUMBER | 13 |  |
| 숙박 | `facilScp` | 시설규모 | `FCLT_SCL` | 시설규모 | NUMBER | 9 |  |
| 숙박 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 숙박 | `infobEn` | 안내소유무 |  |  |  |  | 삭제 |
| 숙박 | `yangsilCnt` | 양실수 | `WSRM_CNT` | 양실수 | NUMBER | 5 |  |
| 숙박 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 숙박 | `engStnTrnmNm` | 영문상호명 | `ENG_CONM_NM` | 영문상호명 | VARCHAR2 | 100 |  |
| 숙박 | `engStnTrnmAddr` | 영문상호주소 | `ENG_CONM_ADDR` | 영문상호주소 | VARCHAR2 | 300 |  |
| 숙박 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 숙박 | `dispenEn` | 의무실유무 |  |  |  |  | 삭제 |
| 숙박 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 숙박 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 숙박 | `cndPermStYmd` | 조건부허가시작일자 | `CNDNAL_PRMSN_BGNG_YMD` | 조건부허가시작일자 | VARCHAR2 | 8 |  |
| 숙박 | `cndPermNtWhy` | 조건부허가신고사유 | `CNDNAL_PRMSN_DCLR_RSN` | 조건부허가신고사유 | VARCHAR2 | 200 |  |
| 숙박 | `cndPermEndYmd` | 조건부허가종료일자 | `CNDNAL_PRMSN_END_YMD` | 조건부허가종료일자 | VARCHAR2 | 8 |  |
| 숙박 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 숙박 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 숙박 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 숙박 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 숙박 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 숙박 | `hanshilCnt` | 한실수 | `KSRM_CNT` | 한실수 | NUMBER | 5 |  |
| 숙박 | `meetSamTimeSygStf` | 회의실별동시수용인원 | `CFRM_PER_CNCR_ACTC_PERNE` | 회의실별동시수용인원 | NUMBER | 10 |  |
| 숙박 | `trstLodgClNm` | 관광숙박업상세명 | `TOUR_LDGBIZ_DTL_NM` | 관광숙박업상세명 | VARCHAR2 | 200 |  |
| 숙박 | `gasLkAlarmCnt` | 가스누설경보기대수 | `GAS_LKGE_ALARM_CNTOM` | 가스누설경보기대수 | NUMBER | 3 |  |
| 숙박 | `bdngFormSeNm` | 건물형태구분명 | `BLDG_SHP_SE_NM` | 건물형태구분명 | VARCHAR2 | 200 |  |
| 숙박 | `singWarnSensorNum` | 단독경보형감지기개수 | `SNGL_ALRMTYP_SENSO_NUM` | 단독경보형감지기개수 | NUMBER | 3 |  |
| 숙박 | `roomArPprt` | 방면적비율 | `RA_AREA_RT` | 방면적비율 | NUMBER | 13 |  |
| 숙박 | `extgCnt` | 소화기개수 | `FIEX_NUM` | 소화기개수 | NUMBER | 13 |  |
| 숙박 | `sewDealFacilCap` | 오수처리시설용량 | `WSWT_PRCS_FCLT_CPCT` | 오수처리시설용량 | NUMBER | 13 |  |
| 숙박 | `desclflnCnt` | 완강기대수 | `DECEN_CNTOM` | 완강기대수 | NUMBER | 3 |  |
| 숙박 | `srvRegn` | 용도지역 | `USG_RGN` | 용도지역 | VARCHAR2 | 500 |  |
| 숙박 | `gdncCoverCnt` | 유도표지개수 | `ESC_CVR_NUM` | 유도표지개수 | NUMBER | 3 |  |
| 숙박 | `carmonSensorCnt` | 일산화탄소감지기대수 | `CBMX_SENSO_CNTOM` | 일산화탄소감지기대수 | NUMBER | 3 |  |
| 숙박 | `autoDistribExtgCnt` | 자동확산소화기대수 | `AUTO_DIFSI_FIEX_CNTOM` | 자동확산소화기대수 | NUMBER | 3 |  |
| 숙박 | `bfaPrvdYnNm` | 조식제공여부 | `BRFT_PVSN_YN` | 조식제공여부 | CHAR | 1 |  |
| 숙박 | `housAr` | 주택면적 | `HSAR` | 주택면적 | NUMBER | 19,9 |  |
| 숙박 | `evzoneGdncCnt` | 피난구유도등개수 | `EE_EMLI_NUM` | 피난구유도등개수 | NUMBER | 3 |  |
| 숙박 | `toilNum` | 화장실수 | `RSTRM_CNT` | 화장실수 | NUMBER | 3 |  |
| 숙박 | `toilFormSeNm` | 화장실종류명 | `RSTRM_KND_NM` | 화장실종류명 | VARCHAR2 | 200 |  |
| 숙박 | `hndEmerLghtCnt` | 휴대용비상조명등대수 | `PRTB_EMRGC_LGTS_CNTOM` | 휴대용비상조명등대수 | NUMBER | 3 |  |
| 숙박 | `chairCnt` | 좌석수 | `SEAT_CNT` | 좌석수 | NUMBER | 14 |  |
| 여행 | `stroomCnt` | 객실수 | `GSRM_CNT` | 객실수 | NUMBER | 10 |  |
| 여행 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 여행 | `cnstYarea` | 건축연면적 | `ARCH_TFA` | 건축연면적 | NUMBER | 18 |  |
| 여행 | `svnSr` | 기념품종류 | `SVNR_KND` | 기념품종류 | VARCHAR2 | 100 |  |
| 여행 | `plnInsurStdt` | 기획여행보험시작일자 | `PLNNG_TRVL_INSRNC_BGNG_YMD` | 기획여행보험시작일자 | VARCHAR2 | 8 |  |
| 여행 | `plnInsurEnddt` | 기획여행보험종료일자 | `PLNNG_TRVL_INSRNC_END_YMD` | 기획여행보험종료일자 | VARCHAR2 | 8 |  |
| 여행 | `playUtsCntDtl` | 놀이기구수내역 |  |  |  |  | 삭제 |
| 여행 | `playFacilCnt` | 놀이시설수 |  |  |  |  | 삭제 |
| 여행 | `stageAr` | 무대면적 | `STAGE_AREA` | 무대면적 | NUMBER | 13 |  |
| 여행 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 여행 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 여행 | `geicpFacilEn` | 발전시설유무 |  |  |  |  | 삭제 |
| 여행 | `bcFacilEn` | 방송시설유무 |  |  |  |  | 삭제 |
| 여행 | `insurOrgNm` | 보험기관명 | `INSRNC_INST_NM` | 보험기관명 | VARCHAR2 | 200 |  |
| 여행 | `insurStdt` | 보험시작일자 | `INSRNC_BGNG_YMD` | 보험시작일자 | CHAR | 8 |  |
| 여행 | `insurEnddt` | 보험종료일자 | `INSRNC_END_YMD` | 보험종료일자 | CHAR | 8 |  |
| 여행 | `afc` | 부대시설내역 |  |  |  |  | 삭제 |
| 여행 | `shpInfo` | 선박제원 | `VSL_SPEC` | 선박제원 | VARCHAR2 | 100 |  |
| 여행 | `shpCnt` | 선박척수 | `VSL_SCNT_CNT` | 선박척수 | NUMBER | 1 |  |
| 여행 | `shpTotTons` | 선박총톤수 | `VSL_TOTAL_TON` | 선박총톤수 | NUMBER | 13 |  |
| 여행 | `facilScp` | 시설규모 | `FCLT_SCL` | 시설규모 | NUMBER | 9 |  |
| 여행 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 여행 | `infobEn` | 안내소유무 |  |  |  |  | 삭제 |
| 여행 | `engStnTrnmNm` | 영문상호명 | `ENG_CONM_NM` | 영문상호명 | VARCHAR2 | 100 |  |
| 여행 | `engStnTrnmAddr` | 영문상호주소 | `ENG_CONM_ADDR` | 영문상호주소 | VARCHAR2 | 300 |  |
| 여행 | `dispenEn` | 의무실유무 |  |  |  |  | 삭제 |
| 여행 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 여행 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 여행 | `chairCnt` | 좌석수 | `SEAT_CNT` | 좌석수 | NUMBER | 14 |  |
| 여행 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 여행 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 여행 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 여행 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 여행 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 여행 | `meetSamTimeSygStf` | 회의실별동시수용인원 | `CFRM_PER_CNCR_ACTC_PERNE` | 회의실별동시수용인원 | NUMBER | 10 |  |
| 여행 | `wrkrRegNo` | 사업자등록번호 | `BRNO` | 사업자등록번호 | CHAR | 10 |  |
| 영화 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 영화 | `perplaFormSeNm` | 공연장형태구분명 | `PRFRPLC_SHP_SE_NM` | 공연장형태구분명 | VARCHAR2 | 200 |  |
| 영화 | `bfGameOcptEctCobNm` | 기존게임업외업종명 |  |  |  |  | 삭제 |
| 영화 | `noroomCnt` | 노래방실수 | `KAROOM_RM_CNT` | 노래방실수 | NUMBER | 3 |  |
| 영화 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 영화 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 영화 | `souarFacilYn` | 방음시설여부 |  |  |  |  | 삭제 |
| 영화 | `vdoRetorNm` | 비디오재생기명 |  |  |  |  | 삭제 |
| 영화 | `emerStairYn` | 비상계단여부 |  |  |  |  | 삭제 |
| 영화 | `emexYn` | 비상구여부 |  |  |  |  | 삭제 |
| 영화 | `fireFacilYn` | 소방시설여부 |  |  |  |  | 삭제 |
| 영화 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 영화 | `soundFacilYn` | 음향시설여부 |  |  |  |  | 삭제 |
| 영화 | `autoChaairYn` | 자동환기여부 |  |  |  |  | 삭제 |
| 영화 | `prvdGathinNm` | 제공게임물명 |  |  |  |  | 삭제 |
| 영화 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 영화 | `lghtFacilYn` | 조명시설유무 |  |  |  |  | 삭제 |
| 영화 | `lghtFacilInillu` | 조명시설조도 |  |  |  |  | 삭제 |
| 영화 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 영화 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 영화 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 영화 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 영화 | `bgroomCnt` | 청소년실수 | `JVNILE_RM_CNT` | 청소년실수 | NUMBER | 3 |  |
| 영화 | `bgroomYn` | 청소년실여부 |  |  |  |  | 삭제 |
| 영화 | `totGasysCnt` | 총게임기수 |  |  |  |  | 삭제 |
| 영화 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 영화 | `frstRegTs` | 최초등록시점 | `FRST_REG_PNT` | 최초등록시점 | VARCHAR2 | 14 |  |
| 영화 | `pasgBreth` | 통로너비 | `PASSG_WIDTH` | 통로너비 | NUMBER | 13 |  |
| 영화 | `specLghtYn` | 특수조명여부 |  |  |  |  | 삭제 |
| 영화 | `cnveFacilYn` | 편의시설여부 |  |  |  |  | 삭제 |
| 영화 | `actlNm` | 품목명 |  |  |  |  | 삭제 |
| 음악 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 음악 | `perplaFormSeNm` | 공연장형태구분명 |  |  |  |  | 삭제 |
| 음악 | `bfGameOcptEctCobNm` | 기존게임업외업종명 |  |  |  |  | 삭제 |
| 음악 | `noroomCnt` | 노래방실수 |  |  |  |  | 삭제 |
| 음악 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 음악 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 음악 | `souarFacilYn` | 방음시설여부 |  |  |  |  | 삭제 |
| 음악 | `vdoRetorNm` | 비디오재생기명 |  |  |  |  | 삭제 |
| 음악 | `emerStairYn` | 비상계단여부 |  |  |  |  | 삭제 |
| 음악 | `emexYn` | 비상구여부 |  |  |  |  | 삭제 |
| 음악 | `fireFacilYn` | 소방시설여부 |  |  |  |  | 삭제 |
| 음악 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 음악 | `soundFacilYn` | 음향시설여부 |  |  |  |  | 삭제 |
| 음악 | `autoChaairYn` | 자동환기여부 |  |  |  |  | 삭제 |
| 음악 | `prvdGathinNm` | 제공게임물명 |  |  |  |  | 삭제 |
| 음악 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 음악 | `lghtFacilYn` | 조명시설유무 |  |  |  |  | 삭제 |
| 음악 | `lghtFacilInillu` | 조명시설조도 |  |  |  |  | 삭제 |
| 음악 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 음악 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 음악 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 음악 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 음악 | `bgroomCnt` | 청소년실수 |  |  |  |  | 삭제 |
| 음악 | `bgroomYn` | 청소년실여부 |  |  |  |  | 삭제 |
| 음악 | `totGasysCnt` | 총게임기수 |  |  |  |  | 삭제 |
| 음악 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 음악 | `frstRegTs` | 최초등록시점 |  |  |  |  | 삭제 |
| 음악 | `pasgBreth` | 통로너비 |  |  |  |  | 삭제 |
| 음악 | `specLghtYn` | 특수조명여부 |  |  |  |  | 삭제 |
| 음악 | `cnveFacilYn` | 편의시설여부 |  |  |  |  | 삭제 |
| 음악 | `actlNm` | 품목명 | `ITEM_NM` | 품목명 | VARCHAR2 | 200 |  |
| 미디어 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 미디어 | `perplaFormSeNm` | 공연장형태구분명 |  |  |  |  | 삭제 |
| 미디어 | `bfGameOcptEctCobNm` | 기존게임업외업종명 |  |  |  |  | 삭제 |
| 미디어 | `noroomCnt` | 노래방실수 |  |  |  |  | 삭제 |
| 미디어 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 미디어 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 미디어 | `souarFacilYn` | 방음시설여부 |  |  |  |  | 삭제 |
| 미디어 | `vdoRetorNm` | 비디오재생기명 |  |  |  |  | 삭제 |
| 미디어 | `emerStairYn` | 비상계단여부 |  |  |  |  | 삭제 |
| 미디어 | `emexYn` | 비상구여부 |  |  |  |  | 삭제 |
| 미디어 | `fireFacilYn` | 소방시설여부 |  |  |  |  | 삭제 |
| 미디어 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 미디어 | `trdCtn` | 영업내용 | `SALS_CN` | 영업내용 | VARCHAR2 | 200 |  |
| 미디어 | `soundFacilYn` | 음향시설여부 |  |  |  |  | 삭제 |
| 미디어 | `autoChaairYn` | 자동환기여부 |  |  |  |  | 삭제 |
| 미디어 | `prvdGathinNm` | 제공게임물명 |  |  |  |  | 삭제 |
| 미디어 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 미디어 | `lghtFacilYn` | 조명시설유무 |  |  |  |  | 삭제 |
| 미디어 | `lghtFacilInillu` | 조명시설조도 |  |  |  |  | 삭제 |
| 미디어 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 미디어 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 미디어 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 미디어 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 미디어 | `bgroomCnt` | 청소년실수 |  |  |  |  | 삭제 |
| 미디어 | `bgroomYn` | 청소년실여부 |  |  |  |  | 삭제 |
| 미디어 | `totGasysCnt` | 총게임기수 |  |  |  |  | 삭제 |
| 미디어 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 미디어 | `frstRegTs` | 최초등록시점 |  |  |  |  | 삭제 |
| 미디어 | `pasgBreth` | 통로너비 |  |  |  |  | 삭제 |
| 미디어 | `specLghtYn` | 특수조명여부 |  |  |  |  | 삭제 |
| 미디어 | `cnveFacilYn` | 편의시설여부 |  |  |  |  | 삭제 |
| 미디어 | `actlNm` | 품목명 |  |  |  |  | 삭제 |
| 미용 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 미용 | `bdngJisgFlrCnt` | 건물지상층수 | `BLDG_GRND_FLR_CNT` | 건물지상층수 | NUMBER | 3 |  |
| 미용 | `bdngUnderFlrCnt` | 건물지하층수 | `BLDG_UDGD_FLR_CNT` | 건물지하층수 | NUMBER | 3 |  |
| 미용 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 미용 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 미용 | `useJisgEndFlr` | 사용끝지상층 | `USE_ED_GRND_FLR` | 사용끝지상층 | NUMBER | 3 |  |
| 미용 | `useUnderEndFlr` | 사용끝지하층 | `USE_ED_UDGD_FLR` | 사용끝지하층 | NUMBER | 3 |  |
| 미용 | `useJisgStFlr` | 사용시작지상층 | `USE_BGNG_GRND_FLR` | 사용시작지상층 | NUMBER | 3 |  |
| 미용 | `useUnderStFlr` | 사용시작지하층 | `USE_BGNG_UDGD_FLR` | 사용시작지하층 | NUMBER | 3 |  |
| 미용 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 미용 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 미용 | `chairCnt` | 의자수 | `CHAI_CNT` | 좌석수 | NUMBER | 14 |  |
| 미용 | `cndPermStYmd` | 조건부허가시작일자 | `CNDNAL_PRMSN_BGNG_YMD` | 조건부허가시작일자 | VARCHAR2 | 8 |  |
| 미용 | `cndPermNtWhy` | 조건부허가신고사유 | `CNDNAL_PRMSN_DCLR_RSN` | 조건부허가신고사유 | VARCHAR2 | 200 |  |
| 미용 | `cndPermEndYmd` | 조건부허가종료일자 | `CNDNAL_PRMSN_END_YMD` | 조건부허가종료일자 | VARCHAR2 | 8 |  |
| 미용 | `abedCnt` | 침대수 | `BED_CNT` | 침대수 | NUMBER | 5 |  |
| 이용 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 이용 | `bdngJisgFlrCnt` | 건물지상층수 | `BLDG_GRND_FLR_CNT` | 건물지상층수 | NUMBER | 3 |  |
| 이용 | `bdngUnderFlrCnt` | 건물지하층수 | `BLDG_UDGD_FLR_CNT` | 건물지하층수 | NUMBER | 3 |  |
| 이용 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 이용 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 이용 | `useJisgEndFlr` | 사용끝지상층 | `USE_ED_GRND_FLR` | 사용끝지상층 | NUMBER | 3 |  |
| 이용 | `useUnderEndFlr` | 사용끝지하층 | `USE_ED_UDGD_FLR` | 사용끝지하층 | NUMBER | 3 |  |
| 이용 | `useJisgStFlr` | 사용시작지상층 | `USE_BGNG_GRND_FLR` | 사용시작지상층 | NUMBER | 3 |  |
| 이용 | `useUnderStFlr` | 사용시작지하층 | `USE_BGNG_UDGD_FLR` | 사용시작지하층 | NUMBER | 3 |  |
| 이용 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 이용 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 이용 | `chairCnt` | 의자수 | `CHAI_CNT` | 좌석수 | NUMBER | 14 |  |
| 이용 | `cndPermStYmd` | 조건부허가시작일자 | `CNDNAL_PRMSN_BGNG_YMD` | 조건부허가시작일자 | VARCHAR2 | 8 |  |
| 이용 | `cndPermNtWhy` | 조건부허가신고사유 | `CNDNAL_PRMSN_DCLR_RSN` | 조건부허가신고사유 | VARCHAR2 | 200 |  |
| 이용 | `cndPermEndYmd` | 조건부허가종료일자 | `CNDNAL_PRMSN_END_YMD` | 조건부허가종료일자 | VARCHAR2 | 8 |  |
| 이용 | `abedCnt` | 침대수 | `BED_CNT` | 침대수 | NUMBER | 5 |  |
| 세탁소/빨래방 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 세탁소/빨래방 | `bdngJisgFlrCnt` | 건물지상층수 | `BLDG_GRND_FLR_CNT` | 건물지상층수 | NUMBER | 3 |  |
| 세탁소/빨래방 | `bdngUnderFlrCnt` | 건물지하층수 | `BLDG_UDGD_FLR_CNT` | 건물지하층수 | NUMBER | 3 |  |
| 세탁소/빨래방 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 세탁소/빨래방 | `sjYn` | 다른 겸업 여부 |  |  |  |  | 삭제 |
| 세탁소/빨래방 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 세탁소/빨래방 | `useJisgEndFlr` | 사용끝지상층 | `USE_ED_GRND_FLR` | 사용끝지상층 | NUMBER | 3 |  |
| 세탁소/빨래방 | `useUnderEndFlr` | 사용끝지하층 | `USE_ED_UDGD_FLR` | 사용끝지하층 | NUMBER | 3 |  |
| 세탁소/빨래방 | `useJisgStFlr` | 사용시작지상층 | `USE_BGNG_GRND_FLR` | 사용시작지상층 | NUMBER | 3 |  |
| 세탁소/빨래방 | `useUnderStFlr` | 사용시작지하층 | `USE_BGNG_UDGD_FLR` | 사용시작지하층 | NUMBER | 3 |  |
| 세탁소/빨래방 | `washmcCnt` | 세탁기수 | `WSMC_CNT` | 세탁기수 | NUMBER | 5 |  |
| 세탁소/빨래방 | `medKind` | 수리대상 의료기기의 유형 |  |  |  |  | 삭제 |
| 세탁소/빨래방 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 세탁소/빨래방 | `trdScp` | 영업규모 |  |  |  |  | 삭제 |
| 세탁소/빨래방 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 세탁소/빨래방 | `cndPermStYmd` | 조건부허가시작일자 | `CNDNAL_PRMSN_BGNG_YMD` | 조건부허가시작일자 | VARCHAR2 | 8 |  |
| 세탁소/빨래방 | `cndPermNtWhy` | 조건부허가신고사유 | `CNDNAL_PRMSN_DCLR_RSN` | 조건부허가신고사유 | VARCHAR2 | 200 |  |
| 세탁소/빨래방 | `cndPermEndYmd` | 조건부허가종료일자 | `CNDNAL_PRMSN_END_YMD` | 조건부허가종료일자 | VARCHAR2 | 8 |  |
| 세탁소/빨래방 | `totScp` | 총규모 | `TOTAL_SCL` | 총규모 | VARCHAR2 | 4000 |  |
| 세탁소/빨래방 | `rcvDrynCnt` | 회수건조기수 | `RTRVL_DYER_CNT` | 회수건조기수 | NUMBER | 3 |  |
| 급식 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 급식 | `fctyOwkEpCnt` | 공장사무직직원수 | `FCTRY_OFJB_EMP_CNT` | 공장사무직직원수 | NUMBER | 8 |  |
| 급식 | `fctyPdtJobEpCnt` | 공장생산직직원수 | `FCTRY_PRODWK_EMP_CNT` | 공장생산직직원수 | NUMBER | 8 |  |
| 급식 | `fctySilJobEpCnt` | 공장판매직직원수 | `FCTRY_SLSPOS_EMP_CNT` | 공장판매직직원수 | NUMBER | 8 |  |
| 급식 | `wtrSplyFacilSeNm` | 급수시설구분명 | `WTRSPPL_FCLT_SE_NM` | 급수시설구분명 | VARCHAR2 | 200 |  |
| 급식 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 급식 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 급식 | `lvSeNm` | 등급구분명 | `GRD_SE_NM` | 등급구분명 | VARCHAR2 | 200 |  |
| 급식 | `isreAm` | 보증액 | `GRNAMT` | 보증액 | NUMBER | 13 |  |
| 급식 | `hoffEpCnt` | 본사직원수 | `HDOFC_EMP_CNT` | 본사직원수 | NUMBER | 8 |  |
| 급식 | `facilTotScp` | 시설총규모 | `FCLT_TOTAL_SCL` | 시설총규모 | VARCHAR2 | 4000 |  |
| 급식 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 급식 | `trdpJubnSeNm` | 영업장주변구분명 | `BIZPLC_SURRND_SE_NM` | 영업장주변구분명 | VARCHAR2 | 200 |  |
| 급식 | `monAm` | 월세액 | `MRNT_AMOUNT` | 월세액 | NUMBER | 13 |  |
| 급식 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 급식 | `jtUpsoMainEdf` | 전통업소주된음식 | `TRDTN_BSNSSP_PRINC_FD` | 전통업소주된음식 | VARCHAR2 | 20 |  |
| 급식 | `jtUpsoAsgnNo` | 전통업소지정번호 | `TRDTN_BSNSSP_DSGN_NO` | 전통업소지정번호 | VARCHAR2 | 20 |  |
| 급식 | `totEpNum` | 총직원수 |  |  |  |  | 삭제 |
| 급식 | `homepage` | 홈페이지 | `HPG` | 홈페이지 | VARCHAR2 | 500 |  |
| 식품 제조/가공/판매 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 식품 제조/가공/판매 | `fctyOwkEpCnt` | 공장사무직직원수 | `FCTRY_OFJB_EMP_CNT` | 공장사무직직원수 | NUMBER | 8 |  |
| 식품 제조/가공/판매 | `fctyPdtJobEpCnt` | 공장생산직직원수 | `FCTRY_PRODWK_EMP_CNT` | 공장생산직직원수 | NUMBER | 8 |  |
| 식품 제조/가공/판매 | `fctySilJobEpCnt` | 공장판매직직원수 | `FCTRY_SLSPOS_EMP_CNT` | 공장판매직직원수 | NUMBER | 8 |  |
| 식품 제조/가공/판매 | `rgtMbdSno` | 권리주체일련번호 | `RGHT_MNBD_SN` | 권리주체일련번호 | VARCHAR2 | 3 |  |
| 식품 제조/가공/판매 | `wtrSplyFacilSeNm` | 급수시설구분명 | `WTRSPPL_FCLT_SE_NM` | 급수시설구분명 | VARCHAR2 | 200 |  |
| 식품 제조/가공/판매 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 식품 제조/가공/판매 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 식품 제조/가공/판매 | `lvSeNm` | 등급구분명 | `GRD_SE_NM` | 등급구분명 | VARCHAR2 | 200 |  |
| 식품 제조/가공/판매 | `isreAm` | 보증액 | `GRNAMT` | 보증액 | NUMBER | 13 |  |
| 식품 제조/가공/판매 | `hoffEpCnt` | 본사직원수 | `HDOFC_EMP_CNT` | 본사직원수 | NUMBER | 8 |  |
| 식품 제조/가공/판매 | `equSiz` | 설비규격 | `TL_SPCFCT` | 설비규격 | VARCHAR2 | 60 |  |
| 식품 제조/가공/판매 | `facilTotScp` | 시설총규모 | `FCLT_TOTAL_SCL` | 시설총규모 | VARCHAR2 | 4000 |  |
| 식품 제조/가공/판매 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 식품 제조/가공/판매 | `trdpJubnSeNm` | 영업장주변구분명 | `BIZPLC_SURRND_SE_NM` | 영업장주변구분명 | VARCHAR2 | 200 |  |
| 식품 제조/가공/판매 | `monAm` | 월세액 | `MRNT_AMOUNT` | 월세액 | NUMBER | 13 |  |
| 식품 제조/가공/판매 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 식품 제조/가공/판매 | `jtUpsoMainEdf` | 전통업소주된음식 | `TRDTN_BSNSSP_PRINC_FD` | 전통업소주된음식 | VARCHAR2 | 20 |  |
| 식품 제조/가공/판매 | `jtUpsoAsgnNo` | 전통업소지정번호 | `TRDTN_BSNSSP_DSGN_NO` | 전통업소지정번호 | VARCHAR2 | 20 |  |
| 식품 제조/가공/판매 | `totEpNum` | 총직원수 | `TNOEMP` | 총직원수 | VARCHAR2 | 20 |  |
| 식품 제조/가공/판매 | `lindPrcbGbnNm` | 축산물가공업구분명 | `LSPRD_PRCSNBIZ_SE_NM` | 축산물가공업구분명 | VARCHAR2 | 500 |  |
| 식품 제조/가공/판매 | `lindJobGbnNm` | 축산업무구분명 | `ANMLHSBNDR_TASK_SE_NM` | 축산업무구분명 | VARCHAR2 | 200 |  |
| 식품 제조/가공/판매 | `lindSeqNo` | 축산일련번호 | `ANMLHSBNDR_SN` | 축산일련번호 | NUMBER | 9 |  |
| 식품 제조/가공/판매 | `homepage` | 홈페이지 | `HPG` | 홈페이지 | VARCHAR2 | 500 |  |
| 유흥주점/단란주점 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 유흥주점/단란주점 | `fctyOwkEpCnt` | 공장사무직직원수 | `FCTRY_OFJB_EMP_CNT` | 공장사무직직원수 | NUMBER | 8 |  |
| 유흥주점/단란주점 | `fctyPdtJobEpCnt` | 공장생산직직원수 | `FCTRY_PRODWK_EMP_CNT` | 공장생산직직원수 | NUMBER | 8 |  |
| 유흥주점/단란주점 | `fctySilJobEpCnt` | 공장판매직직원수 | `FCTRY_SLSPOS_EMP_CNT` | 공장판매직직원수 | NUMBER | 8 |  |
| 유흥주점/단란주점 | `wtrSplyFacilSeNm` | 급수시설구분명 | `WTRSPPL_FCLT_SE_NM` | 급수시설구분명 | VARCHAR2 | 200 |  |
| 유흥주점/단란주점 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 유흥주점/단란주점 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 유흥주점/단란주점 | `lvSeNm` | 등급구분명 | `GRD_SE_NM` | 등급구분명 | VARCHAR2 | 200 |  |
| 유흥주점/단란주점 | `isreAm` | 보증액 | `GRNAMT` | 보증액 | NUMBER | 13 |  |
| 유흥주점/단란주점 | `hoffEpCnt` | 본사직원수 | `HDOFC_EMP_CNT` | 본사직원수 | NUMBER | 8 |  |
| 유흥주점/단란주점 | `facilTotScp` | 시설총규모 | `FCLT_TOTAL_SCL` | 시설총규모 | VARCHAR2 | 4000 |  |
| 유흥주점/단란주점 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 유흥주점/단란주점 | `trdpJubnSeNm` | 영업장주변구분명 | `BIZPLC_SURRND_SE_NM` | 영업장주변구분명 | VARCHAR2 | 200 |  |
| 유흥주점/단란주점 | `monAm` | 월세액 | `MRNT_AMOUNT` | 월세액 | NUMBER | 13 |  |
| 유흥주점/단란주점 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 유흥주점/단란주점 | `jtUpsoMainEdf` | 전통업소주된음식 | `TRDTN_BSNSSP_PRINC_FD` | 전통업소주된음식 | VARCHAR2 | 20 |  |
| 유흥주점/단란주점 | `jtUpsoAsgnNo` | 전통업소지정번호 | `TRDTN_BSNSSP_DSGN_NO` | 전통업소지정번호 | VARCHAR2 | 20 |  |
| 유흥주점/단란주점 | `totEpNum` | 총직원수 |  |  |  |  | 삭제 |
| 유흥주점/단란주점 | `homepage` | 홈페이지 | `HPG` | 홈페이지 | VARCHAR2 | 500 |  |
| 음식점 | `stroomCnt` | 객실수 | `GSRM_CNT` | 객실수 | NUMBER | 10 |  |
| 음식점 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 음식점 | `bdngSrvNm` | 건물용도명 | `BLDG_USG_NM` | 건물용도명 | VARCHAR2 | 100 |  |
| 음식점 | `cnstYarea` | 건축연면적 | `ARCH_TFA` | 건축연면적 | NUMBER | 18 |  |
| 음식점 | `fctyOwkEpCnt` | 공장사무직직원수 | `FCTRY_OFJB_EMP_CNT` | 공장사무직직원수 | NUMBER | 8 |  |
| 음식점 | `fctyPdtJobEpCnt` | 공장생산직직원수 | `FCTRY_PRODWK_EMP_CNT` | 공장생산직직원수 | NUMBER | 8 |  |
| 음식점 | `fctySilJobEpCnt` | 공장판매직직원수 | `FCTRY_SLSPOS_EMP_CNT` | 공장판매직직원수 | NUMBER | 8 |  |
| 음식점 | `wtrSplyFacilSeNm` | 급수시설구분명 | `WTRSPPL_FCLT_SE_NM` | 급수시설구분명 | VARCHAR2 | 200 |  |
| 음식점 | `svnSr` | 기념품종류 | `SVNR_KND` | 기념품종류 | VARCHAR2 | 100 |  |
| 음식점 | `plnInsurStdt` | 기획여행보험시작일자 |  |  |  |  | 삭제 |
| 음식점 | `plnInsurEnddt` | 기획여행보험종료일자 |  |  |  |  | 삭제 |
| 음식점 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 음식점 | `playUtsCntDtl` | 놀이기구수내역 |  |  |  |  | 삭제 |
| 음식점 | `playFacilCnt` | 놀이시설수 |  |  |  |  | 삭제 |
| 음식점 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 음식점 | `lvSeNm` | 등급구분명 | `GRD_SE_NM` | 등급구분명 | VARCHAR2 | 200 |  |
| 음식점 | `stageAr` | 무대면적 | `STAGE_AREA` | 무대면적 | NUMBER | 13 |  |
| 음식점 | `culWrkrSeNm` | 문화사업자구분명 | `CULTR_BZMN_SE_NM` | 문화사업자구분명 | VARCHAR2 | 200 |  |
| 음식점 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 음식점 | `geicpFacilEn` | 발전시설유무 |  |  |  |  | 삭제 |
| 음식점 | `bcFacilEn` | 방송시설유무 |  |  |  |  | 삭제 |
| 음식점 | `isreAm` | 보증액 | `GRNAMT` | 보증액 | NUMBER | 13 |  |
| 음식점 | `insurOrgNm` | 보험기관명 | `INSRNC_INST_NM` | 보험기관명 | VARCHAR2 | 200 |  |
| 음식점 | `insurStdt` | 보험시작일자 | `INSRNC_BGNG_YMD` | 보험시작일자 | CHAR | 8 |  |
| 음식점 | `insurEnddt` | 보험종료일자 | `INSRNC_END_YMD` | 보험종료일자 | CHAR | 8 |  |
| 음식점 | `hoffEpCnt` | 본사직원수 | `HDOFC_EMP_CNT` | 본사직원수 | NUMBER | 8 |  |
| 음식점 | `afc` | 부대시설내역 |  |  |  |  | 삭제 |
| 음식점 | `shpInfo` | 선박제원 | `VSL_SPEC` | 선박제원 | VARCHAR2 | 100 |  |
| 음식점 | `shpCnt` | 선박척수 | `VSL_SCNT_CNT` | 선박척수 | NUMBER | 1 |  |
| 음식점 | `shpTotTons` | 선박총톤수 | `VSL_TOTAL_TON` | 선박총톤수 | NUMBER | 13 |  |
| 음식점 | `facilScp` | 시설규모 | `FCLT_SCL` | 시설규모 | NUMBER | 9 |  |
| 음식점 | `facilAr` | 시설면적 | `FCAR` | 시설면적 | NUMBER | 19,9 |  |
| 음식점 | `facilTotScp` | 시설총규모 | `FCLT_TOTAL_SCL` | 시설총규모 | VARCHAR2 | 4000 |  |
| 음식점 | `infobEn` | 안내소유무 |  |  |  |  | 삭제 |
| 음식점 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 음식점 | `engStnTrnmNm` | 영문상호명 | `ENG_CONM_NM` | 영문상호명 | VARCHAR2 | 100 |  |
| 음식점 | `engStnTrnmAddr` | 영문상호주소 | `ENG_CONM_ADDR` | 영문상호주소 | VARCHAR2 | 300 |  |
| 음식점 | `trdpJubnSeNm` | 영업장주변구분명 | `BIZPLC_SURRND_SE_NM` | 영업장주변구분명 | VARCHAR2 | 200 |  |
| 음식점 | `monAm` | 월세액 | `MRNT_AMOUNT` | 월세액 | NUMBER | 13 |  |
| 음식점 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 음식점 | `dispenEn` | 의무실유무 |  |  |  |  | 삭제 |
| 음식점 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 음식점 | `jtUpsoMainEdf` | 전통업소주된음식 | `TRDTN_BSNSSP_PRINC_FD` | 전통업소주된음식 | VARCHAR2 | 20 |  |
| 음식점 | `jtUpsoAsgnNo` | 전통업소지정번호 | `TRDTN_BSNSSP_DSGN_NO` | 전통업소지정번호 | VARCHAR2 | 20 |  |
| 음식점 | `mnfacTreArtclCn` | 제작취급품목내용 | `FBCTN_HNDL_ITEM_CN` | 제작취급품목내용 | VARCHAR2 | 200 |  |
| 음식점 | `chairCnt` | 좌석수 | `SEAT_CNT` | 좌석수 | NUMBER | 14 |  |
| 음식점 | `nearEnvNm` | 주변환경명 | `SURRND_ENVRNMNT_NM` | 주변환경명 | VARCHAR2 | 200 |  |
| 음식점 | `jisgNumLay` | 지상층수 | `GRND_NOFL` | 지상층수 | NUMBER | 3 |  |
| 음식점 | `regnSeNm` | 지역구분명 | `RGN_SE_NM` | 지역구분명 | VARCHAR2 | 200 |  |
| 음식점 | `underNumLay` | 지하층수 | `UDGD_NOFL` | 지하층수 | NUMBER | 3 |  |
| 음식점 | `totEpNum` | 총직원수 |  |  |  |  | 삭제 |
| 음식점 | `totNumLay` | 총층수 | `TOTAL_NOFL` | 총층수 | NUMBER | 3 |  |
| 음식점 | `homepage` | 홈페이지 | `HPG` | 홈페이지 | VARCHAR2 | 500 |  |
| 음식점 | `meetSamTimeSygStf` | 회의실별동시수용인원 | `CFRM_PER_CNCR_ACTC_PERNE` | 회의실별동시수용인원 | NUMBER | 10 |  |
| 유통 | `bcTotAm` | 부채총액 | `LBLT_TOTA` | 부채총액 | NUMBER | 15 |  |
| 유통 | `wrkrRegNo` | 사업자등록번호 | `BRNO` | 사업자등록번호 | CHAR | 10 |  |
| 유통 | `cobGbnNm` | 업종구분명 | `TPBIZ_SE_NM` | 업종구분명 | VARCHAR2 | 200 |  |
| 유통 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 유통 | `captScale` | 자본금의규모 | `CPTL_OF_SCL` | 자본금의규모 | NUMBER | 15 |  |
| 유통 | `asetScp` | 자산규모 | `AST_SCL` | 자산규모 | NUMBER | 15 |  |
| 유통 | `jpSeNm` | 점포구분명 | `STOR_SE_NM` | 점포구분명 | VARCHAR2 | 200 |  |
| 유통 | `silMetNm` | 판매방식명 | `NTSL_MTH_NM` | 판매방식명 | VARCHAR2 | 300 |  |
| 목재 | `ytPdtQy` | 년간생산량 | `ANUU_PRDQ` | 년간생산량 | NUMBER | 13 |  |
| 목재 | `tmbSeNm` | 목재생산업구분코드명 | `WD_PRDCTNBIZ_SE_CD_NM` | 목재생산업구분코드명 | VARCHAR2 | 200 |  |
| 목재 | `tmbSrNm` | 목재생산업종류명 | `WD_PRDCTNBIZ_KND_NM` | 목재생산업종류명 | VARCHAR2 | 200 |  |
| 목재 | `stateSeNm` | 상태구분명 | `STTS_SE_NM` | 상태구분명 | VARCHAR2 | 200 |  |
| 목재 | `mpwKeeSitu` | 인력보유현황 | `MNPW_HLD_PRST` | 인력보유현황 | VARCHAR2 | 250 |  |
| 목재 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 목재 | `treTmbrPrdt` | 취급목재제품 | `HNDL_WD_PRDCT` | 취급목재제품 | VARCHAR2 | 1000 |  |
| 에너지 | `gasPdtSortNm` | 가스용품종류명 |  |  |  |  | 삭제 |
| 에너지 | `gasSortNm` | 가스종류명 | `GAS_KND_NM` | 가스종류명 | VARCHAR2 | 100 |  |
| 에너지 | `upchNm` | 거래처 | `CNPT` | 거래처 | VARCHAR2 | 200 |  |
| 에너지 | `supRulesCtn` | 공급규정내용 | `SPLY_RULE_CN` | 공급규정내용 | VARCHAR2 | 250 |  |
| 에너지 | `ltChgCn` | 길이변경내용 | `LEN_CHG_CN` | 길이변경내용 | VARCHAR2 | 200 |  |
| 에너지 | `exmRan` | 면제범위 |  |  |  |  | 삭제 |
| 에너지 | `prdSiz` | 물품규격 |  |  |  |  | 삭제 |
| 에너지 | `baeLt` | 배관길이 | `PIPE_LEN` | 배관길이 | VARCHAR2 | 20 |  |
| 에너지 | `baeEsbPlc` | 배관설치장소 | `PIPE_INSTL_PLC` | 배관설치장소 | VARCHAR2 | 250 |  |
| 에너지 | `offTelno` | 사무소전화번호 | `OFCE_TELNO` | 사무소전화번호 | VARCHAR2 | 20 |  |
| 에너지 | `ofeAr` | 사무실면적 | `OFC_AREA` | 사무실면적 | NUMBER | 13 |  |
| 에너지 | `bsnsOpeningPreArrYmd` | 사업개시예정일자 | `BIZ_STRT_PRNMNT_YMD` | 사업개시예정일자 | VARCHAR2 | 8 |  |
| 에너지 | `wrkpGrdSrvSeNm` | 사업장부지용도구분명 | `BPLC_SIE_USG_SE_NM` | 사업장부지용도구분명 | VARCHAR2 | 200 |  |
| 에너지 | `wrkpTelno` | 사업장전화번호 | `BPLC_TELNO` | 사업장전화번호 | VARCHAR2 | 20 |  |
| 에너지 | `useObj` | 사용목적 | `USE_PRPS` | 사용목적 | VARCHAR2 | 4000 |  |
| 에너지 | `useMet` | 사용방법 | `USE_MTHD` | 사용방법 | VARCHAR2 | 2000 |  |
| 에너지 | `dsnrSpvsnSortNm` | 설계감리업종류명 | `DESIGN_SPVSBIZ_KND_NM` | 설계감리업종류명 | VARCHAR2 | 200 |  |
| 에너지 | `equNm` | 설비명 |  |  |  |  | 삭제 |
| 에너지 | `staNm` | 소속국가명 | `OGDP_NTN_NM` | 소속국가명 | VARCHAR2 | 200 |  |
| 에너지 | `sygRglstCnt` | 수용정원수 | `ACTC_PSCP_CNT` | 수용정원수 | NUMBER | 13 |  |
| 에너지 | `facilUseYn` | 시설사용여부 |  |  |  |  | 삭제 |
| 에너지 | `realCapt` | 실질자본금 | `ACTCL_CPTL` | 실질자본금 | NUMBER | 13 |  |
| 에너지 | `cobGbnNm` | 업종구분명 | `TPBIZ_SE_NM` | 업종구분명 | VARCHAR2 | 200 |  |
| 에너지 | `instrStoroomAr` | 용기저장실면적 | `CNTNR_STRR_AREA` | 용기저장실면적 | NUMBER | 13 |  |
| 에너지 | `bmonUseQy` | 월사용량 | `MM_USQTY` | 월사용량 | NUMBER | 13 |  |
| 에너지 | `cyprPdtFacil` | 윤전기생산시설 | `RP_PRDCTN_FCLT` | 윤전기생산시설 | VARCHAR2 | 300 |  |
| 에너지 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 에너지 | `saveEquLoc` | 저장설비위치 | `STRG_TL_PSTN` | 저장설비위치 | VARCHAR2 | 250 |  |
| 에너지 | `scoalAr` | 저탄장면적 | `CYA_AREA` | 저탄장면적 | NUMBER | 30 |  |
| 에너지 | `prdSeNm` | 제조구분명 | `MNFTR_SE_NM` | 제조구분명 | VARCHAR2 | 200 |  |
| 에너지 | `cgpAr` | 차고지면적 | `GAR_AREA` | 차고지면적 | NUMBER | 13 |  |
| 에너지 | `rlServlnEnNm` | 철도인입선유무명 | `RAIWA_INLN_EN_NM` | 철도인입선유무명 | VARCHAR2 | 200 |  |
| 에너지 | `treGasCap` | 취급가스용량 | `HNDL_GAS_CPCT` | 취급가스용량 | NUMBER | 10 |  |
| 지하수 | `facilEqi` | 시설장비 | `FCLT_EQPMNT` | 시설장비 | VARCHAR2 | 1000 |  |
| 지하수 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 지하수 | `specMpwTotNum` | 전문인력총수 | `SPCLMNPW_TOTAL_CNT` | 전문인력총수 | NUMBER | 9 |  |
| 지하수 | `otrOrgTransYn` | 타기관이전여부 | `OINST_BFR_YN` | 타기관이전여부 | VARCHAR2 | 1 |  |
| 환경관리 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 환경관리 | `bdngJisgFlrCnt` | 건물지상층수 | `BLDG_GRND_FLR_CNT` | 건물지상층수 | NUMBER | 3 |  |
| 환경관리 | `bdngUnderFlrCnt` | 건물지하층수 | `BLDG_UDGD_FLR_CNT` | 건물지하층수 | NUMBER | 3 |  |
| 환경관리 | `bdngNm` | 건축물명 | `BDST_NM` | 건축물명 | VARCHAR2 | 100 |  |
| 환경관리 | `bdngStateNm` | 건축물상태명 | `BDST_STTS_NM` | 건축물상태명 | VARCHAR2 | 200 |  |
| 환경관리 | `bdngYarea` | 건축물연면적 | `BDST_TFA` | 건축물연면적 | NUMBER | 13 |  |
| 환경관리 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 환경관리 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 환경관리 | `dynpwSprayNum` | 동력분무기수 | `MOTOR_SPRY_CNT` | 동력분무기수 | NUMBER | 5 |  |
| 환경관리 | `gmkNum` | 방독면수 | `GSMASK_CNT` | 방독면수 | NUMBER | 5 |  |
| 환경관리 | `pvtFacilYearOprDaycnt` | 방지시설연간가동일수 | `PRVNTN_FCLT_ANL_OPRTNG_DAY_CNT` | 방지시설연간가동일수 | NUMBER | 3 |  |
| 환경관리 | `pvtFacilOprtnPd` | 방지시설조업시간 | `PRVNTN_FCLT_WRK_HR` | 방지시설조업시간 | VARCHAR2 | 12 |  |
| 환경관리 | `discFacilYearOprDaycnt` | 배출시설연간가동일수 | `EMSN_FCLT_ANL_OPRTNG_DAY_CNT` | 배출시설연간가동일수 | NUMBER | 3 |  |
| 환경관리 | `discFacilOprtnPd` | 배출시설조업시간 | `EMSN_FCLT_WRK_HR` | 배출시설조업시간 | VARCHAR2 | 12 |  |
| 환경관리 | `protGlsNum` | 보호안경수 | `PRTC_GLSSS_CNT` | 보호안경수 | NUMBER | 5 |  |
| 환경관리 | `protUseClotNum` | 보호용의복수 | `PRTCAPRL_CNT` | 보호용의복수 | NUMBER | 5 |  |
| 환경관리 | `ofeAr` | 사무실면적 | `OFC_AREA` | 사무실면적 | NUMBER | 13 |  |
| 환경관리 | `#N/A` | 사업자등록번호 | `BRNO` | 사업자등록번호 | CHAR | 10 |  |
| 환경관리 | `apvPermSeNm` | 사업장구분명 | `BPLC_SE_NM` | 사업장구분명 | VARCHAR2 | 100 |  |
| 환경관리 | `useJisgEndFlr` | 사용끝지상층 | `USE_ED_GRND_FLR` | 사용끝지상층 | NUMBER | 3 |  |
| 환경관리 | `useUnderEndFlr` | 사용끝지하층 | `USE_ED_UDGD_FLR` | 사용끝지하층 | NUMBER | 3 |  |
| 환경관리 | `useJisgStFlr` | 사용시작지상층 | `USE_BGNG_GRND_FLR` | 사용시작지상층 | NUMBER | 3 |  |
| 환경관리 | `useUnderStFlr` | 사용시작지하층 | `USE_BGNG_UDGD_FLR` | 사용시작지하층 | NUMBER | 3 |  |
| 환경관리 | `disfetVehGarAr` | 소독차량차고면적 | `DSNFCT_VHCL_GRG_AREA` | 소독차량차고면적 | NUMBER | 13 |  |
| 환경관리 | `site` | 소재지 | `LCTN` | 소재지 | VARCHAR2 | 200 |  |
| 환경관리 | `hdoptdSprayNum` | 수동식분무기수 | `MANL_SPRY_CNT` | 수동식분무기수 | NUMBER | 5 |  |
| 환경관리 | `applYmd` | 신청일자 | `APLY_YMD` | 신청일자 | CHAR | 8 |  |
| 환경관리 | `labRdnBdngOriNo` | 실험실도로명주소건물본번호 | `LAB_ROAD_NM_ADDR_BLDGMNO` | 실험실도로명주소건물본번호 | VARCHAR2 | 5 |  |
| 환경관리 | `labRdnBdngSubNo` | 실험실도로명주소건물부번호 | `LAB_ROAD_NM_ADDR_BLDGSNO` | 실험실도로명주소건물부번호 | VARCHAR2 | 5 |  |
| 환경관리 | `labRdnBdngFlrGbn` | 실험실도로명주소건물층구분 | `LAB_ROAD_NM_ADDR_BLDG_FLR_SE` | 실험실도로명주소건물층구분 | VARCHAR2 | 1 |  |
| 환경관리 | `labRdnCggCode` | 실험실도로명주소시군구코드 | `LAB_ROAD_NM_ADDR_SGG_CD` | 실험실도로명주소시군구코드 | VARCHAR2 | 5 |  |
| 환경관리 | `labRdnPostNo` | 실험실도로명주소우편번호 | `LAB_ROAD_NM_ADDR_ZIP` | 실험실도로명주소우편번호 | VARCHAR2 | 6 |  |
| 환경관리 | `labRdnUmdGbn` | 실험실도로명주소읍면동구분 | `LAB_ROAD_NM_ADDR_EMD_SE` | 실험실도로명주소읍면동구분 | VARCHAR2 | 1 |  |
| 환경관리 | `labRdnUmdCode` | 실험실도로명주소읍면동코드 | `LAB_ROAD_NM_ADDR_EMD_CD` | 실험실도로명주소읍면동코드 | VARCHAR2 | 10 |  |
| 환경관리 | `labRdnCode` | 실험실도로명주소코드 | `LAB_ROAD_NM_ADDR_CD` | 실험실도로명주소코드 | VARCHAR2 | 7 |  |
| 환경관리 | `labRdnSpecAddr` | 실험실도로명특수주소 | `LAB_ROAD_NM_SPCL_ADDR` | 실험실도로명특수주소 | VARCHAR2 | 200 |  |
| 환경관리 | `labAr` | 실험실면적 | `LAB_AREA` | 실험실면적 | NUMBER | 13 |  |
| 환경관리 | `labBan` | 실험실반 | `LAB_BAN` | 실험실반 | VARCHAR2 | 3 |  |
| 환경관리 | `labBunji` | 실험실번지 | `LAB_LOTNB` | 실험실번지 | VARCHAR2 | 20 |  |
| 환경관리 | `labSan` | 실험실산 | `LAB_MTN` | 실험실산 | VARCHAR2 | 1 |  |
| 환경관리 | `labPostNo` | 실험실우편번호 | `LAB_ZIP` | 실험실우편번호 | VARCHAR2 | 6 |  |
| 환경관리 | `labRegnCode` | 실험실지역코드 | `LAB_RGN_CD` | 실험실지역코드 | VARCHAR2 | 10 |  |
| 환경관리 | `labTong` | 실험실통 | `LAB_TONG` | 실험실통 | VARCHAR2 | 3 |  |
| 환경관리 | `labSpecAddr` | 실험실특수주소 | `LAB_SPCL_ADDR` | 실험실특수주소 | VARCHAR2 | 90 |  |
| 환경관리 | `labSpecDng` | 실험실특수주소동 | `LAB_SPCL_ADDR_TR` | 실험실특수주소동 | VARCHAR2 | 20 |  |
| 환경관리 | `labSpecHo` | 실험실특수주소호 | `LAB_SPCL_ADDR_UNI` | 실험실특수주소호 | VARCHAR2 | 10 |  |
| 환경관리 | `labHo` | 실험실호 | `LAB_UNI` | 실험실호 | VARCHAR2 | 4 |  |
| 환경관리 | `bsnGbn` | 업무구분 | `TASK_SE` | 업무구분 | VARCHAR2 | 2 |  |
| 환경관리 | `bsnGbnNm` | 업무구분명 | `TASK_SE_NM` | 업무구분명 | VARCHAR2 | 100 |  |
| 환경관리 | `upsoSeNm` | 업소구분명 | `BSNSSP_SE_NM` | 업소구분명 | VARCHAR2 | 200 |  |
| 환경관리 | `cobGbnNm` | 업종구분명 | `TPBIZ_SE_NM` | 업종구분명 | VARCHAR2 | 200 |  |
| 환경관리 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 환경관리 | `trdplAr` | 영업소면적 | `BIZOFC_AREA` | 영업소면적 | NUMBER | 13 |  |
| 환경관리 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 환경관리 | `truUpchNm` | 위탁업체명 | `CNSGN_BZENTY_NM` | 위탁업체명 | VARCHAR2 | 100 |  |
| 환경관리 | `cndPermStYmd` | 조건부허가시작일자 | `CNDNAL_PRMSN_BGNG_YMD` | 조건부허가시작일자 | VARCHAR2 | 8 |  |
| 환경관리 | `cndPermNtWhy` | 조건부허가신고사유 | `CNDNAL_PRMSN_DCLR_RSN` | 조건부허가신고사유 | VARCHAR2 | 200 |  |
| 환경관리 | `cndPermEndYmd` | 조건부허가종료일자 | `CNDNAL_PRMSN_END_YMD` | 조건부허가종료일자 | VARCHAR2 | 8 |  |
| 환경관리 | `jongGbnNm` | 종별명 | `BTP_NM` | 종별명 | VARCHAR2 | 200 |  |
| 환경관리 | `pdtAtclNm` | 주생산품명 | `PRMN_PRDT_NM` | 주생산품명 | VARCHAR2 | 200 |  |
| 환경관리 | `asgnYmd` | 지정일자 | `DSGN_YMD` | 지정일자 | CHAR | 8 |  |
| 환경관리 | `epCnt` | 직원수 | `EMP_CNT` | 직원수 | VARCHAR2 | 20 |  |
| 환경관리 | `vacuClerNum` | 진공청소기수 | `VAC_VACCLR_CNT` | 진공청소기수 | NUMBER | 5 |  |
| 환경관리 | `clsTgtStdt` | 청소대상시작일자 | `CLNNG_TRGT_BGNG_YMD` | 청소대상시작일자 | VARCHAR2 | 8 |  |
| 환경관리 | `clsTgtEnddt` | 청소대상종료일자 | `CLNNG_TRGT_END_YMD` | 청소대상종료일자 | VARCHAR2 | 8 |  |
| 환경관리 | `microSpklNum` | 초미립자살포기수 | `ULV_SPR_CNT` | 초미립자살포기수 | NUMBER | 5 |  |
| 환경관리 | `abwSeNm` | 폐기물구분명 | `WASTE_SE_NM` | 폐기물구분명 | VARCHAR2 | 200 |  |
| 환경관리 | `abwDealOcptSeNm` | 폐기물처리업구분명 | `WASTE_PRCSBIZ_SE_NM` | 폐기물처리업구분명 | VARCHAR2 | 200 |  |
| 환경관리 | `abwDealOcptCbDealSeNm` | 폐기물처리업별처리구분명 | `WASTE_PRCSBIZ_PER_PRCS_SE_NM` | 폐기물처리업별처리구분명 | VARCHAR2 | 200 |  |
| 환경관리 | `asgnmtList1` | 항목값1 | `ARTCL_VL_1` | 항목값1 | VARCHAR2 | 255 |  |
| 환경관리 | `permGiganStdt` | 허가기간_시작일자 | `PRMSN_PRD_BGNG_YMD` | 허가기간시작일자 | VARCHAR2 | 8 |  |
| 환경관리 | `permGiganEnddt` | 허가기간_종료일자 | `PRMSN_PRD_END_YMD` | 허가기간종료일자 | VARCHAR2 | 8 |  |
| 환경관리 | `permDepoQy` | 허용보관량 | `PRM_KPNGQTY` | 허용보관량 | NUMBER | 13 |  |
| 환경관리 | `permDepoCn` | 허용보관량내용 | `PRM_KPNGQTY_CN` | 허용보관량내용 | VARCHAR2 | 2000 |  |
| 환경관리 | `envBsnSeNm` | 환경업무구분명 | `ENVRNMNT_TASK_SE_NM` | 환경업무구분명 | VARCHAR2 | 200 |  |
| 환경관리 | `hndUseStlzNum` | 휴대용소독기수 | `PRTB_STLZ_CNT` | 휴대용소독기수 | NUMBER | 5 |  |
| 환경관리 | `casWhy` | 휴업폐지사유 | `TCBIZ_ABL_RSN` | 휴업폐지사유 | VARCHAR2 | 500 |  |
| 체육 | `bdngDngNum` | 건축물동수 | `BDST_BICOU` | 건축물동수 | NUMBER | 5 |  |
| 체육 | `bdngYarea` | 건축물연면적 | `BDST_TFA` | 건축물연면적 | NUMBER | 13 |  |
| 체육 | `puprSeNm` | 공사립구분명 | `PBP_SE_NM` | 공사립구분명 | VARCHAR2 | 200 |  |
| 체육 | `culPhyedCobNm` | 문화체육업종명 | `CULTR_SPTS_TPBIZ_NM` | 문화체육업종명 | VARCHAR2 | 200 |  |
| 체육 | `bupNm` | 법인명 | `CORP_NM` | 법인명 | VARCHAR2 | 100 |  |
| 체육 | `insurJnYnCode` | 보험가입여부코드 | `INSRNC_JOIN_YN_CD` | 보험가입여부코드 | VARCHAR2 | 1 |  |
| 체육 | `drmkCobNm` | 세부업종명 | `DTIL_TPBIZ_NM` | 세부업종명 | VARCHAR2 | 200 |  |
| 체육 | `lderCnt` | 지도자수 | `LDER_CNT` | 지도자수 | NUMBER | 5 |  |
| 체육 | `drmAr` | 탈의실면적 | `CHARM_AREA` | 탈의실면적 | NUMBER | 13 |  |
| 체육 | `rerAr` | 휴게실면적 | `LNGE_AREA` | 휴게실면적 | NUMBER | 13 |  |
| 체육 | `ofeAr` | 사무실면적 | `OFC_AREA` | 사무실면적 | NUMBER | 13 |  |
| 체육 | `memCollTotStfNum` | 회원모집총인원 | `MBR_RCRT_TOTAL_PERNE` | 회원모집총인원 | NUMBER | 9 |  |
| 담배 | `tbcoSpyUpchNm` | 담배공급업체명 | `CGRTT_SPLY_BZENTY_NM` | 담배공급업체명 | VARCHAR2 | 255 |  |
| 담배 | `mwSrNm` | 민원종류명 | `CVLCPT_KND_NM` | 민원종류명 | VARCHAR2 | 100 |  |
| 담배 | `asgnYmd` | 지정일자 | `DSGN_YMD` | 지정일자 | CHAR | 8 |  |
| 담배 | `trePrdtNm` | 취급제품명 | `HNDL_PRDCT_NM` | 취급제품명 | VARCHAR2 | 255 |  |
| 목욕탕/찜질방/사우나 | `bdngOwnSeNm` | 건물소유구분명 | `BLDG_PSN_SE_NM` | 건물소유구분명 | VARCHAR2 | 200 |  |
| 목욕탕/찜질방/사우나 | `bdngJisgFlrCnt` | 건물지상층수 | `BLDG_GRND_FLR_CNT` | 건물지상층수 | NUMBER | 3 |  |
| 목욕탕/찜질방/사우나 | `bdngUnderFlrCnt` | 건물지하층수 | `BLDG_UDGD_FLR_CNT` | 건물지하층수 | NUMBER | 3 |  |
| 목욕탕/찜질방/사우나 | `manEipCnt` | 남성종사자수 | `ML_PRCTR_CNT` | 남성종사자수 | NUMBER | 8 |  |
| 목욕탕/찜질방/사우나 | `multUsnUpsoYn` | 다중이용업소여부 | `MLT_UTZTN_BSNSSP_YN` | 다중이용업소여부 | VARCHAR2 | 1 |  |
| 목욕탕/찜질방/사우나 | `balhansilYn` | 발한실여부 | `SWEATRM_YN` | 발한실여부 | VARCHAR2 | 1 |  |
| 목욕탕/찜질방/사우나 | `useJisgEndFlr` | 사용끝지상층 | `USE_ED_GRND_FLR` | 사용끝지상층 | NUMBER | 3 |  |
| 목욕탕/찜질방/사우나 | `useUnderEndFlr` | 사용끝지하층 | `USE_ED_UDGD_FLR` | 사용끝지하층 | NUMBER | 3 |  |
| 목욕탕/찜질방/사우나 | `useJisgStFlr` | 사용시작지상층 | `USE_BGNG_GRND_FLR` | 사용시작지상층 | NUMBER | 3 |  |
| 목욕탕/찜질방/사우나 | `useUnderStFlr` | 사용시작지하층 | `USE_BGNG_UDGD_FLR` | 사용시작지하층 | NUMBER | 3 |  |
| 목욕탕/찜질방/사우나 | `wmEipCnt` | 여성종사자수 | `FML_PRCTR_CNT` | 여성종사자수 | NUMBER | 8 |  |
| 목욕탕/찜질방/사우나 | `yoksilCnt` | 욕실수 | `BTHRM_CNT` | 욕실수 | NUMBER | 14 |  |
| 목욕탕/찜질방/사우나 | `sntUptaeNm` | 위생업태명 | `SNTTN_BZSTAT_NM` | 위생업태명 | VARCHAR2 | 200 |  |
| 목욕탕/찜질방/사우나 | `cndPermStYmd` | 조건부허가시작일자 | `CNDNAL_PRMSN_BGNG_YMD` | 조건부허가시작일자 | VARCHAR2 | 8 |  |
| 목욕탕/찜질방/사우나 | `cndPermNtWhy` | 조건부허가신고사유 | `CNDNAL_PRMSN_DCLR_RSN` | 조건부허가신고사유 | VARCHAR2 | 200 |  |
| 목욕탕/찜질방/사우나 | `cndPermEndYmd` | 조건부허가종료일자 | `CNDNAL_PRMSN_END_YMD` | 조건부허가종료일자 | VARCHAR2 | 8 |  |
| 물류 | `frzWareDngNum` | 냉동_냉장창고_동수 | `FRZN_RFRG_WRHUS_TR_CNT` | 냉동냉장창고동수 | VARCHAR2 | 5 |  |
| 물류 | `frzWareArea` | 냉동_냉장창고_면적 | `FRZN_RFRG_WRHUS_AREA` | 냉동냉장창고면적 | VARCHAR2 | 200 |  |
| 물류 | `licEfgiStdt` | 면허유효기간시작일자 | `LCNS_VLD_PRD_BGNG_YMD` | 면허유효기간시작일자 | VARCHAR2 | 8 |  |
| 물류 | `licEfgiEnddt` | 면허유효기간종료일자 | `LCNS_VLD_PRD_END_YMD` | 면허유효기간종료일자 | VARCHAR2 | 8 |  |
| 물류 | `licYmd` | 면허일자 | `LCNS_YMD` | 면허일자 | VARCHAR2 | 8 |  |
| 물류 | `bupYnNm` | 법인여부명 | `CORP_YN_NM` | 법인여부명 | VARCHAR2 | 200 |  |
| 물류 | `depoPer` | 보관요율 | `KPNG_TRF` | 보관요율 | VARCHAR2 | 100 |  |
| 물류 | `depoPlcArea` | 보관장소_면적 | `KPNG_PLC_AREA` | 보관장소면적 | VARCHAR2 | 20 |  |
| 물류 | `facilEqiDtl` | 시설/장비현황 | `FCLT_EQPMNT_PRST` | 시설/장비현황 | VARCHAR2 | 1000 |  |
| 물류 | `upchKindNm` | 업체유형명 | `BZENTY_TYPE_NM` | 업체유형명 | VARCHAR2 | 300 |  |
| 물류 | `uptaeDepoWare` | 업태_보관및창고업 | `BZSTAT_KPNG_WRHUSBIZ` | 업태보관및창고업 | VARCHAR2 | 1 |  |
| 물류 | `uptaeTran` | 업태_운송및택배업 | `BZSTAT_TRANS_PRLBIZ` | 업태운송및택배업 | VARCHAR2 | 1 |  |
| 물류 | `uptaeMaker` | 업태_제조업 | `BZSTAT_MFBIZ` | 업태제조업 | VARCHAR2 | 1 |  |
| 물류 | `uptaeSale` | 업태_판매업 | `BZSTAT_NTSLBIZ` | 업태판매업 | VARCHAR2 | 1 |  |
| 물류 | `genWareDngNum` | 일반창고_동수 | `GNRL_WRHUS_TR_CNT` | 일반창고동수 | VARCHAR2 | 5 |  |
| 물류 | `genWareArea` | 일반창고_면적 | `GNRL_WRHUS_AREA` | 일반창고면적 | VARCHAR2 | 18 |  |
| 물류 | `qalIssueOrgCode` | 자격면허발급기관 | `QLFC_LCNS_ISSU_INST` | 자격면허발급기관 | VARCHAR2 | 60 |  |
| 물류 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 물류 | `sfTeamCode` | 자치단체코드 | `LGLGOV_CD` | 자치단체코드 | VARCHAR2 | 7 |  |
| 물류 | `asgnAdjtCobNm` | 지정정비업종명 | `DSGN_MTNC_TPBIZ_NM` | 지정정비업종명 | VARCHAR2 | 200 |  |
| 물류 | `epCnt` | 직원수 | `EMP_CNT` | 직원수 | VARCHAR2 | 20 |  |
| 민방위(급수시설) | `emerFacilLoc` | 비상시설위치 | `EMRGC_FCLT_PSTN` | 비상시설위치 | VARCHAR2 | 250 |  |
| 민방위(급수시설) | `facilSeNm` | 시설구분명 | `FCLT_SE_NM` | 시설구분명 | VARCHAR2 | 50 |  |
| 민방위(급수시설) | `facilNmBdngNm` | 시설명_건물명 | `FCLT_NM_BLDG_NM` | 시설명건물명 | VARCHAR2 | 250 |  |
| 민방위(급수시설) | `dsvYmd` | 해제일자 | `RMV_YMD` | 해제일자 | CHAR | 8 |  |
| 상조 | `depucOrgEtcNm` | 공제계약기타명 | `DDC_CTRT_ETC_NM` | 공제계약기타명 | VARCHAR2 | 255 |  |
| 상조 | `depucOrgNm` | 공제계약명 | `DDC_CTRT_NM` | 공제계약명 | VARCHAR2 | 200 |  |
| 상조 | `mwSrNm` | 민원종류명 | `CVLCPT_KND_NM` | 민원종류명 | VARCHAR2 | 100 |  |
| 상조 | `insur` | 보험 | `INSRNC` | 보험 | VARCHAR2 | 255 |  |
| 상조 | `wrkrRegNo` | 사업자등록번호 | `BRNO` | 사업자등록번호 | CHAR | 10 |  |
| 상조 | `depBankNm` | 예치기관명 | `DEPST_INST_NM` | 예치기관명 | VARCHAR2 | 200 |  |
| 상조 | `captScale` | 자본금의 규모 | `CPTL_OF_SCL` | 자본금의규모 | NUMBER | 15 |  |
| 상조 | `debtPayIsre` | 채무지급보증 | `DBT_GIVE_GRNTE` | 채무지급보증 | VARCHAR2 | 255 |  |
| 엘리베이터 | `elvGbnNm` | 관리업구분명 | `MNGBIZ_SE_NM` | 관리업구분명 | VARCHAR2 | 500 |  |
| 엘리베이터 | `funcStfCnt` | 기능직직원수 | `TCJB_EMP_CNT` | 기능직직원수 | VARCHAR2 | 20 |  |
| 엘리베이터 | `tecianStfCnt` | 기술직직원수 | `ENJB_EMP_CNT` | 기술직직원수 | VARCHAR2 | 20 |  |
| 엘리베이터 | `etcStfCnt` | 기타직원수 | `ETC_EMP_CNT` | 기타직원수 | VARCHAR2 | 20 |  |
| 엘리베이터 | `rprRan` | 보수범위 | `COMP_SCP` | 보수범위 | VARCHAR2 | 30 |  |
| 엘리베이터 | `afrStfCnt` | 사무직직원수 | `OFJB_EMP_CNT` | 사무직직원수 | VARCHAR2 | 20 |  |
| 엘리베이터 | `dsnDutyTecMpw` | 설계책임기술인력수 | `DESIGN_RSP_TECH_MNPW_CNT` | 설계책임기술인력수 | VARCHAR2 | 10 |  |
| 엘리베이터 | `paffTecianCnt` | 실무기술인력수 | `PRCWK_TECH_MNPW_CNT` | 실무기술인력수 | VARCHAR2 | 10 |  |
| 엘리베이터 | `cobGbnNm` | 업종구분명 | `TPBIZ_SE_NM` | 업종구분명 | VARCHAR2 | 200 |  |
| 엘리베이터 | `rprDutyManCnt` | 유지관리책임인력수 | `UPKP_MNG_RSP_MNPW` | 유지관리책임인력수 | VARCHAR2 | 10 |  |
| 엘리베이터 | `ofcrCnt` | 임원수 | `EXC_CNT` | 임원수 | VARCHAR2 | 20 |  |
| 엘리베이터 | `capt` | 자본금 | `CPTL` | 자본금 | VARCHAR2 | 15 |  |
| 엘리베이터 | `propNm` | 자산 | `AST` | 자산 | VARCHAR2 | 200 |  |
| 엘리베이터 | `prdDutyTecMpw` | 제조책임기술인력수 | `MNFTR_RSP_TECH_MNPW` | 제조책임기술인력수 | VARCHAR2 | 10 |  |
| 엘리베이터 | `totStfCnt` | 총직원수 | `TNOEMP` | 총직원수 | VARCHAR2 | 20 |  |
| 엘리베이터 | `cmpnySeNm` | 회사구분명 | `CO_SE_NM` | 회사구분명 | VARCHAR2 | 200 |  |
| 엘리베이터 | `wrkrRegNo` | 사업자등록번호 | `BRNO` | 사업자등록번호 | CHAR | 10 |  |
| 엘리베이터 | `cmpnySeCode` | 회사구분코드 | `CO_SE_CD` | 회사구분코드 | VARCHAR2 | 2 |  |
| 전문교육기관 | `naepdSuppYn` | 국비지원여부 |  |  |  |  | 삭제 |
| 전문교육기관 | `chrStfCn` | 담당직원내용 |  |  |  |  | 삭제 |
| 전문교육기관 | `licNm` | 보유자격증명 |  |  |  |  | 삭제 |
| 전문교육기관 | `deleteYmd` | 삭제일자 | `DEL_YMD` | 삭제일자 | CHAR | 8 |  |
| 사무지원 | `seNm` | 구분명 | `SE_NM` | 구분명 | VARCHAR2 | 100 |  |
| 사무지원 | `bupGbnNm` | 법인구분명 | `CORP_SE_NM` | 법인구분명 | VARCHAR2 | 200 |  |
| 무인민원발급기 | `opnSvcId` | 개방서비스ID |  |  |  |  | 삭제 |
| 무인민원발급기 | `opnSfTeamCode` | 개방자치단체코드 | `OPN_ATMY_GRP_CD` | 개방자치단체코드 | CHAR | 7 |  |
| 무인민원발급기 | `mgtNo` | 관리번호 | `MNG_NO` | 관리번호 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `opnSfTeamNm` | 관리기관명 | `MNG_INST_NM` | 관리기관명 | VARCHAR2 | 200 |  |
| 무인민원발급기 | `kioskNm기` | 발급기명 | `ISSUMCHN_NM` | 발급기명 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `esbPlcAddr` | 설치장소주소 | `INSTL_PLC_ADDR` | 설치장소주소 | VARCHAR2 | 200 |  |
| 무인민원발급기 | `esbPlcDetailL` | 설치장소상세위치 | `INSTL_PLC_DTL_PSTN` | 설치장소상세위치 | VARCHAR2 | 255 |  |
| 무인민원발급기 | `wdayStHm` | 평일운영시작시각 | `WKDY_OPER_BGNG_TM` | 평일운영시작시각 | CHAR | 4 |  |
| 무인민원발급기 | `wdayEndHm` | 평일운영종료시각 | `WKDY_OPER_END_TM` | 평일운영종료시각 | CHAR | 4 |  |
| 무인민원발급기 | `holidayStHm` | 공휴일운영시작시각 | `LHLDY_OPER_BGNG_TM` | 공휴일운영시작시각 | CHAR | 4 |  |
| 무인민원발급기 | `holidayEndHm` | 공휴일운영종료시각 | `LHLDY_OPER_END_TM` | 공휴일운영종료시각 | CHAR | 4 |  |
| 무인민원발급기 | `kioskHmRfnCn` | 운영시간참고내용 | `OPER_HR_REF_CN` | 운영시간참고내용 | VARCHAR2 | 255 |  |
| 무인민원발급기 | `esbMngUrl` | 설치운영URL | `INSTL_OPER_URL` | 설치운영URL | VARCHAR2 | 500 |  |
| 무인민원발급기 | `useYnNm` | 사용여부명 | `USE_YN_NM` | 사용여부명 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `kioskFormNm` | 장애인편의기능정보 | `PWDBS_CVN_ISSUMCHN_SHP` | 장애인편의기능정보 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `obspHdinMtNm` | 시각장애인용키패드 | `FRBLND_KPD` | 시각장애인용키패드 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `obspVoiceGdNm` | 시각장애인용음성안내 | `FRBLND_VOICE_GD` | 시각장애인용음성안내 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `obspCovpGdNm` | 청각장애인용화면안내 | `FRDEAF_SCRN_GD` | 청각장애인용화면안내 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `obspBrailNm` | 점자라벨부착 | `BRL_LBL_ATCMNT` | 점자라벨부착 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `extrVoiceMtNm` | 이어폰소켓 | `EPHN_SCKT` | 이어폰소켓 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `obspBrailMntN` | 촉각(전자)모니터 | `TCTL_ELCTNC_MONITOR` | 촉각(전자)모니터 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `pgEnlgFuncNm` | 화면확대기능 | `SCRN_EXPSN_FWK` | 화면확대기능 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `obspTrChairNm` | 휠체어사용자조작 | `WHCHR_USER_MNPLT` | 휠체어사용자조작 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `lastModTs` | 최종수정시점 | `LAST_MDFCN_PNT` | 최종수정시점 | VARCHAR2 | 14 |  |
| 무인민원발급기 | `updateGbn` | 데이터갱신구분 | `DAT_UPDT_SE` | 데이터갱신구분 | CHAR | 1 |  |
| 무인민원발급기 | `updateDt` | 데이터갱신일자 | `DAT_UPDT_PNT` | 데이터갱신시점 | VARCHAR2 | 14 |  |
| 무인민원발급기 | `sidoCode` | 시도코드 | `CTPV_CD` | 시도코드 | CHAR | 7 |  |
| 무인민원발급기 | `esbPlcLoc` | 설치장소위치 | `INSTL_PLC_PSTN` | 설치장소위치 | VARCHAR2 | 100 |  |
| 무인민원발급기 | `rdCggCd` | 도로시군구코드 | `ROAD_SGG_CD` | 도로시군구코드 | VARCHAR2 | 5 |  |
| 무인민원발급기 | `rdCd` | 도로코드 | `ROAD_CD` | 도로코드 | VARCHAR2 | 7 |  |
| 무인민원발급기 | `rdnUmdNo` | 도로명읍면동번호 | `ROAD_NM_EMD_NO` | 도로명읍면동번호 | VARCHAR2 | 3 |  |
| 무인민원발급기 | `rdBdngFlrSe` | 도로건물층구분 | `ROAD_BLDG_FLR_SE` | 도로건물층구분 | CHAR | 1 |  |
| 무인민원발급기 | `rdBdngOriNo` | 도로건물본번호 | `ROAD_BLDGMNO` | 도로건물본번호 | VARCHAR2 | 5 |  |
| 무인민원발급기 | `rdBdngSubNo` | 도로건물부번호 | `ROAD_BLDGSNO` | 도로건물부번호 | VARCHAR2 | 5 |  |
| 무인민원발급기 | `regtItemPrfdocIssueGbb` | 등기사항증명서발급구분 | `RG_MTTR_PRDOC_ISSU_SE` | 등기사항증명서발급구분 | VARCHAR2 | 50 |  |
| 무인민원발급기 | `fmlyRelsDeleteIssueGb` | 가족관계삭제발급구분 | `FAM_REL_DEL_ISSU_SE` | 가족관계삭제발급구분 | VARCHAR2 | 50 |  |
| 민방위대피시설 | `opnSfTeamCode` | 개방자치단체코드 | `OPN_ATMY_GRP_CD` | 개방자치단체코드 | CHAR | 7 |  |
| 민방위대피시설 | `mgtNo` | 관리번호 | `MNG_NO` | 관리번호 | VARCHAR2 | 50 |  |
| 민방위대피시설 | `asgnYmd` | 지정일자 | `DSGN_YMD` | 지정일자 | CHAR | 8 |  |
| 민방위대피시설 | `dsvYmd` | 해제일자 | `RMV_YMD` | 해제일자 | CHAR | 8 |  |
| 민방위대피시설 | `dsvGb` | 운영상태 | `OPER_STTS` | 운영상태 | VARCHAR2 | 10 |  |
| 민방위대피시설 | `facilSeNm` | 시설명 | `FCLT_NM` | 시설명 | VARCHAR2 | 256 |  |
| 민방위대피시설 | `facilNmBdngNm` | 시설구분 | `FCLT_SE` | 시설구분 | VARCHAR2 | 50 |  |
| 민방위대피시설 | `rdnWhlAddr` | 도로명전체주소 | `ROAD_NM_WHOL_ADDR` | 도로명전체주소 | VARCHAR2 | 500 |  |
| 민방위대피시설 | `siteAddr` | 소재지전체주소 | `LCTN_WHOL_ADDR` | 소재지전체주소 | VARCHAR2 | 500 |  |
| 민방위대피시설 | `rdnPostNo` | 도로명우편번호 | `ROAD_NM_ZIP` | 도로명우편번호 | CHAR | 5 |  |
| 민방위대피시설 | `jisgUnderSeNm` | 시설위치(지상/지하) | `FCLTLOC_GRND_UDGD` | 시설위치(지상/지하) | VARCHAR2 | 10 |  |
| 민방위대피시설 | `siteArea` | 시설면적(㎡) | `FCLT_AREA` | 시설면적(㎡) | VARCHAR2 | 18 |  |
| 민방위대피시설 | `useCanStfCnt` | 최대수용인원 | `MAX_ACTC_PERNE` | 최대수용인원 | VARCHAR2 | 9 |  |
| 민방위대피시설 | `lastModTs` | 최종수정시점 | `LAST_MDFCN_PNT` | 최종수정시점 | VARCHAR2 | 14 |  |
| 민방위대피시설 | `updateGbn` | 데이터갱신구분 | `DAT_UPDT_SE` | 데이터갱신구분 | CHAR | 1 |  |
| 민방위대피시설 | `updateDt` | 데이터갱신일자 | `DAT_UPDT_PNT` | 데이터갱신시점 | VARCHAR2 | 14 |  |
| 민방위대피시설 | `facilLade` | 위도(도) | `LAT_DEGR` | 위도(도) | NUMBER | 2 |  |
| 민방위대피시설 | `facilLami` | 위도(분) | `LAT_MINT` | 위도(분) | NUMBER | 2 |  |
| 민방위대피시설 | `facilLase` | 위도(초) | `LAT_SEC` | 위도(초) | NUMBER | 7,4 |  |
| 민방위대피시설 | `facilLode` | 경도(도) | `LOT_DEGR` | 경도(도) | NUMBER | 3 |  |
| 민방위대피시설 | `facilLomi` | 경도(분) | `LOT_MINT` | 경도(분) | NUMBER | 2 |  |
| 민방위대피시설 | `facilLose` | 경도(초) | `LOT_SEC` | 경도(초) | NUMBER | 7,4 |  |
| 민방위대피시설 | `wgs84Epsg4326` | 위도(EPSG4326) | `LAT_EPSG4326` | 위도(EPSG4326) | VARCHAR2 | 14 |  |
| 민방위대피시설 | `wgs84Epsg4326` | 경도(EPSG4326) | `LOT_EPST4326` | 경도(EPSG4326) | VARCHAR2 | 14 |  |
| 민방위대피시설 | `utmKEpsg5179X` | 좌표정보X(EPSG5179) | `CRD_INFO_X_EPSG5179` | 좌표정보X(EPSG5179) | VARCHAR2 | 30 |  |
| 민방위대피시설 | `utmKEpsg5179Y` | 좌표정보Y(EPSG5179) | `CRD_INFO_Y_EPSG5179` | 좌표정보Y(EPSG5179) | VARCHAR2 | 30 |  |
