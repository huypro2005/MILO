*==============================================================================
* DE TAI: Tac dong cua FDI den phat thai CO2 - vai tro dieu tiet cua chat luong
*         the che (73 nuoc dang phat trien, 2002-2022)
* Tac gia: Vo Thi Linh Nhi
* Do-file tai lap pipeline Python (code/s01 -> s10), theo knowledge/SPEC.md
*
* CACH CHAY: sua duong dan o MUC 0.1 -> Do (Ctrl+D). Ket qua: thu muc stata_out/
* Yeu cau: Stata 15 tro len. Goi cai them o MUC 0.2 (can mang lan chay dau).
*
* Mo hinh (giong file Python):
*   M1 (H1): lnCO2 = FDI + lnY + URB + TO + Crdt + u_i + l_t
*   M2 (H2): M1 + IQk                       (k = CC GE PV RQ RL VA, IQ_PCA)
*   M3 (H3): lnCO2 = FDI_c + IQk_c + FDIxIQk + kiem soat + u_i + l_t
*   Uoc luong CHINH (D18): FEDYNDK = FE dong 2 chieu (them lnCO2 t-1)
*                          + SE Driscoll-Kraay + split-panel jackknife
*==============================================================================

version 15
clear all
set more off
capture log close

*------------------------------------------------------------------------------
* MUC 0. DUONG DAN & GOI CAI THEM
*------------------------------------------------------------------------------
* 0.1 SUA DONG NAY: thu muc chua DATA_FINAL.xlsx
global ROOT "C:/Users/TEN_BAN/Documents/MILO"
cd "$ROOT"
capture mkdir "stata_out"
global OUT "$ROOT/stata_out"
log using "$OUT/log_FDI_CO2.smcl", replace

* 0.2 Goi tu SSC / Stata Journal (tu bo qua neu da cai)
foreach p in xtscc xtabond2 estout xtcsd xttest3 pescadf {
    capture which `p'
    if _rc ssc install `p', replace
}
capture which xtserial
if _rc net install st0039, from("http://www.stata-journal.com/software/sj3-2") replace

*------------------------------------------------------------------------------
* MUC 1. NAP & BIEN DOI DU LIEU (tuong ung code/common.py::load_panel)
*------------------------------------------------------------------------------
import excel using "$ROOT/DATA_FINAL.xlsx", sheet("Sheet1") firstrow clear
encode Country, gen(id)
xtset id Year
xtdescribe                                  // ky vong: 73 nuoc x 21 nam, can bang

gen lnCO2 = ln(CO2)
gen lnY   = ln(Y)
label var lnCO2 "ln CO2 binh quan dau nguoi"
label var FDI   "FDI rong vao (% GDP)"
label var lnY   "ln GDP binh quan dau nguoi"
label var URB   "Do thi hoa (%)"
label var TO    "Do mo thuong mai (% GDP)"
label var Crdt  "Tin dung tu nhan (% GDP)"

* IQ_PCA = thanh phan chinh thu nhat cua 6 WGI chuan hoa; dau sao cho cung chieu WGI
pca CC GE PV RQ RL VA
predict IQ_PCA, score
quietly corr IQ_PCA CC
if r(rho) < 0 replace IQ_PCA = -IQ_PCA
label var IQ_PCA "Chi so the che tong hop (PCA)"

global IQ    "CC GE PV RQ RL VA"
global IQALL "CC GE PV RQ RL VA IQ_PCA"
global CTRL  "lnY URB TO Crdt"
global DCTRL "D_lnY D_URB D_TO D_Crdt"

* Trung tam hoa truoc khi tao bien tuong tac (D3)
quietly summarize FDI
gen FDI_c = FDI - r(mean)
foreach k of global IQALL {
    quietly summarize `k'
    gen `k'_c   = `k' - r(mean)
    gen FDIx`k' = FDI_c * `k'_c
}

* Ban winsorize FDI 1%/99% (kiem dinh vung, D12)
_pctile FDI, p(1 99)
gen FDI_w = min(max(FDI, r(r1)), r(r2))
quietly summarize FDI_w
gen FDI_wc = FDI_w - r(mean)
foreach k of global IQALL {
    gen FDIwx`k' = FDI_wc * `k'_c
}

* Bien tre, sai phan, dummy nam, xu the: tao san (xtscc ban cu khong nhan i., L., D.)
sort id Year
gen L_lnCO2 = L.lnCO2
label var L_lnCO2 "lnCO2 (t-1)"
foreach v in lnCO2 lnY URB TO Crdt {
    gen D_`v' = D.`v'
}
tab Year, gen(yr)
global YD  "yr2-yr21"       // mo hinh tinh: 2002-2022, nam goc 2002
global YDD "yr3-yr21"       // mo hinh dong / sai phan: 2003-2022, nam goc 2003
gen t = Year - 2002
global TR ""
forvalues i = 2/73 {        // xu the rieng tung nuoc; bo nuoc 1 (cong tuyen voi dummy nam)
    gen tr`i' = (id == `i') * t
    global TR "$TR tr`i'"
}

save "$OUT/panel.dta", replace

*------------------------------------------------------------------------------
* MUC 2. THONG KE MO TA (s01)
*------------------------------------------------------------------------------
summarize lnCO2 CO2 FDI $IQ IQ_PCA Y lnY URB TO Crdt, detail
xtsum lnCO2 FDI lnY URB TO Crdt $IQ IQ_PCA        // overall / between / within
estpost summarize lnCO2 FDI lnY URB TO Crdt $IQ IQ_PCA
esttab using "$OUT/T1_mota.rtf", replace label nomtitle nonumber ///
    cells("count mean(fmt(3)) sd(fmt(3)) min(fmt(2)) max(fmt(2))") title("Bang 1. Thong ke mo ta")

*------------------------------------------------------------------------------
* MUC 3. TUONG QUAN & VIF (s02)
*------------------------------------------------------------------------------
pwcorr lnCO2 FDI $IQ IQ_PCA $CTRL, star(0.05)
estpost correlate lnCO2 FDI $IQ IQ_PCA $CTRL, matrix listwise
esttab using "$OUT/T2_tuongquan.rtf", replace unstack not noobs compress b(3) ///
    title("Bang 2. Ma tran tuong quan")

* VIF tung mo hinh (6 WGI dua RIENG tung bien - D6)
quietly regress lnCO2 FDI $CTRL
estat vif
foreach k of global IQALL {
    di as txt _n "---- VIF M2 va M3 voi `k' ----"
    quietly regress lnCO2 FDI `k' $CTRL
    estat vif
    quietly regress lnCO2 FDI_c `k'_c FDIx`k' $CTRL
    estat vif
}
* Minh hoa ly do D6: dua chung 6 WGI -> VIF rat cao
quietly regress lnCO2 FDI $IQ $CTRL
estat vif

*------------------------------------------------------------------------------
* MUC 4. POLS / FE / RE + HAUSMAN (s03) - M1, co dummy nam
*------------------------------------------------------------------------------
eststo clear
eststo POLS: regress lnCO2 FDI $CTRL $YD, vce(cluster id)
eststo FE:   xtreg   lnCO2 FDI $CTRL $YD, fe vce(cluster id)
eststo RE:   xtreg   lnCO2 FDI $CTRL $YD, re vce(cluster id)

* Hausman co dien (SE khong vung)
quietly xtreg lnCO2 FDI $CTRL $YD, fe
estimates store fe_h
quietly xtreg lnCO2 FDI $CTRL $YD, re
estimates store re_h
hausman fe_h re_h, sigmamore

* Hausman vung kieu Mundlak (A4): RE + trung binh nhom cua X, Wald cum theo nuoc
foreach v in FDI $CTRL {
    bysort id (Year): egen m_`v' = mean(`v')
}
sort id Year
quietly xtreg lnCO2 FDI $CTRL m_FDI m_lnY m_URB m_TO m_Crdt $YD, re vce(cluster id)
test m_FDI m_lnY m_URB m_TO m_Crdt          // p < 0,05 -> bac bo RE, dung FE
drop m_*

*------------------------------------------------------------------------------
* MUC 5. KIEM DINH KHUYET TAT (s04) -> FE Driscoll-Kraay (FEDK)
*------------------------------------------------------------------------------
quietly xtreg lnCO2 FDI $CTRL, fe
xttest3                                      // Modified Wald: phuong sai thay doi
xtcsd, pesaran abs                           // Pesaran CD: phu thuoc cheo
xtserial lnCO2 FDI $CTRL                     // Wooldridge: tu tuong quan bac 1

* Nghiem don vi CIPS (Pesaran 2007), 1 tre ADF
pescadf lnCO2, lags(1) trend
pescadf lnY,   lags(1) trend
pescadf FDI,   lags(1)
* Luu y: Python tinh p-value CIPS bang mo phong Monte Carlo (D15b, D21);
* pescadf dung bang gia tri toi han chuan -> ket luan co the lech khi o sat nguong.

* FEDK tinh. Bang thong lag(2) = floor(4*(T/100)^(2/9)), giong linearmodels
eststo FEDK: xtscc lnCO2 FDI $CTRL $YD, fe lag(2)
esttab POLS FE RE FEDK using "$OUT/T3_tinh_H1.rtf", replace b(4) se(4) ///
    star(* 0.10 ** 0.05 *** 0.01) keep(FDI $CTRL) label mtitles("POLS" "FE" "RE" "FE-DK") ///
    title("Bang 3. Mo hinh tinh M1 (H1)") note("Co dummy nam. SE cum theo nuoc (POLS/FE/RE), Driscoll-Kraay (FE-DK).")

eststo clear
foreach k of global IQALL {
    eststo H2_FEDK_`k': xtscc lnCO2 FDI `k' $CTRL $YD, fe lag(2)
}
esttab H2_FEDK_* using "$OUT/T4_FEDK_H2.rtf", replace b(4) se(4) star(* 0.10 ** 0.05 *** 0.01) ///
    drop(yr* _cons) label title("Bang 4. FE-DK tinh - M2 (H2)")

eststo clear
foreach k of global IQALL {
    eststo H3_FEDK_`k': xtscc lnCO2 FDI_c `k'_c FDIx`k' $CTRL $YD, fe lag(2)
}
esttab H3_FEDK_* using "$OUT/T5_FEDK_H3.rtf", replace b(4) se(4) star(* 0.10 ** 0.05 *** 0.01) ///
    drop(yr* _cons) label title("Bang 5. FE-DK tinh - M3 (H3)")

*------------------------------------------------------------------------------
* MUC 6. UOC LUONG CHINH: FEDYNDK + SPLIT-PANEL JACKKNIFE (s10, D18/D23)
*   b_jk = 2*b_day_du - (b_nua1 + b_nua2)/2
*   Nua 1 = 2002-2012, nua 2 = 2012-2022; bien tre tinh trong tung nua nen nam
*   dau moi nua bi mat -> hoi quy tren 2003-2012 va 2013-2022.
*   SE cua jackknife = SE Driscoll-Kraay mau day du (D23a).
*------------------------------------------------------------------------------
capture program drop fedyn_jk
program define fedyn_jk
    * Cu phap: fedyn_jk <ten_luu> <bien giai thich, KHONG gom L_lnCO2>
    gettoken name xs : 0
    * (a) Mau day du, SE Driscoll-Kraay
    xtscc lnCO2 L_lnCO2 `xs' $YDD, fe lag(2)
    estimates store `name'
    tempname b1 b2
    * (b) Hai nua mau, FE 2 chieu (chi can he so)
    quietly xtreg lnCO2 L_lnCO2 `xs' $YDD if inrange(Year, 2003, 2012), fe
    matrix `b1' = e(b)
    quietly xtreg lnCO2 L_lnCO2 `xs' $YDD if inrange(Year, 2013, 2022), fe
    matrix `b2' = e(b)
    quietly estimates restore `name'
    * (c) In bang
    di as txt _n "{hline 86}"
    di as res "JACKKNIFE - `name'"
    di as txt %-13s "Bien" %10s "b (DK)" %9s "SE" %8s "p" %10s "b_jk" %8s "p_jk" %10s "nua 1" %10s "nua 2"
    foreach v in L_lnCO2 `xs' {
        local bf = _b[`v']
        local se = _se[`v']
        local h1 = el(`b1', 1, colnumb(`b1', "`v'"))
        local h2 = el(`b2', 1, colnumb(`b2', "`v'"))
        local bj = 2*`bf' - (`h1' + `h2')/2
        di as txt %-13s abbrev("`v'", 13) as res %10.4f `bf' %9.4f `se' %8.3f 2*normal(-abs(`bf'/`se')) ///
            %10.4f `bj' %8.3f 2*normal(-abs(`bj'/`se')) %10.4f `h1' %10.4f `h2'
        if "`v'" == "L_lnCO2" {
            di as txt "   rho_jk KTC95% = [" %6.3f (`bj' - 1.96*`se') ", " %6.3f (`bj' + 1.96*`se') ///
                "]  (>= 1 -> khong bao cao he so dai han, D25)"
        }
    }
    di as txt "{hline 86}"
end

* H1
fedyn_jk H1_FEDYNDK FDI $CTRL
* H2: 6 WGI + IQ_PCA
foreach k of global IQALL {
    fedyn_jk H2_FEDYNDK_`k' FDI `k' $CTRL
}
* H3: 6 WGI + IQ_PCA (bien trung tam hoa)
foreach k of global IQALL {
    fedyn_jk H3_FEDYNDK_`k' FDI_c `k'_c FDIx`k' $CTRL
}

esttab H1_FEDYNDK H2_FEDYNDK_* using "$OUT/T6_FEDYNDK_H1H2.rtf", replace b(4) se(4) ///
    star(* 0.10 ** 0.05 *** 0.01) drop(yr* _cons) label ///
    title("Bang 6. FE dong + Driscoll-Kraay (uoc luong chinh) - H1, H2")
esttab H3_FEDYNDK_* using "$OUT/T7_FEDYNDK_H3.rtf", replace b(4) se(4) ///
    star(* 0.10 ** 0.05 *** 0.01) drop(yr* _cons) label ///
    title("Bang 7. FE dong + Driscoll-Kraay (uoc luong chinh) - H3")

* He so dai han CHUA hieu chinh - CHI THAM KHAO (D25: rho_jk >= 1 -> khong bao cao)
estimates restore H1_FEDYNDK
nlcom (LR_FDI: _b[FDI] / (1 - _b[L_lnCO2]))

*------------------------------------------------------------------------------
* MUC 7. TAC DONG BIEN CUA FDI THEO CHAT LUONG THE CHE (s06, H3)
*   ME(q) = b_FDI + b_FDIxk * (IQk(q) - mean IQk), q = P10 P25 P50 P75 P90
*------------------------------------------------------------------------------
tempname ME
postfile `ME' str8 iq pct iq_value me se p using "$OUT/marginal_effects.dta", replace
foreach k of global IQALL {
    quietly summarize `k'
    local mk = r(mean)
    _pctile `k', p(10 25 50 75 90)
    forvalues j = 1/5 {
        local x`j' = r(r`j')
    }
    estimates restore H3_FEDYNDK_`k'
    local j = 1
    foreach q in 10 25 50 75 90 {
        local dx = `x`j'' - `mk'
        quietly lincom FDI_c + (`dx')*FDIx`k'
        post `ME' ("`k'") (`q') (`x`j'') (r(estimate)) (r(se)) (2*normal(-abs(r(estimate)/r(se))))
        local ++j
    }
}
postclose `ME'
preserve
use "$OUT/marginal_effects.dta", clear
format iq_value me se %9.4f
format p %6.3f
list, sepby(iq) noobs
export excel using "$OUT/marginal_effects.xlsx", firstrow(variables) replace
restore

*------------------------------------------------------------------------------
* MUC 8. KIEM DINH VUNG (s05, s07)
*------------------------------------------------------------------------------
* 8.1 System GMM 2 buoc, collapse, sai so Windmeijer, dummy nam (D4, D11 - dac ta C0)
*     pydynpd "gmm(lnCO2, 2:4)" <=> xtabond2 "gmm(lnCO2, lag(2 4) collapse)"
*     xtabond2 tu bao AR(1), AR(2), Hansen va Difference-in-Hansen
eststo clear
eststo SGMM_H1: xtabond2 lnCO2 L.lnCO2 FDI $CTRL $YDD, ///
    gmm(lnCO2, lag(2 4) collapse) iv(FDI $CTRL $YDD) twostep robust
foreach k of global IQALL {
    eststo SGMM_H2_`k': xtabond2 lnCO2 L.lnCO2 FDI `k' $CTRL $YDD, ///
        gmm(lnCO2, lag(2 4) collapse) iv(FDI `k' $CTRL $YDD) twostep robust
    eststo SGMM_H3_`k': xtabond2 lnCO2 L.lnCO2 FDI_c `k'_c FDIx`k' $CTRL $YDD, ///
        gmm(lnCO2, lag(2 4) collapse) iv(FDI_c `k'_c FDIx`k' $CTRL $YDD) twostep robust
}
esttab SGMM_* using "$OUT/T8_SGMM.rtf", replace b(4) se(4) star(* 0.10 ** 0.05 *** 0.01) ///
    drop(yr* _cons) scalars("ar1p AR(1) p" "ar2p AR(2) p" "hansenp Hansen p" "j So cong cu") ///
    label title("Bang 8. System GMM (kiem dinh vung)")

* Can Bond: he so lnCO2(t-1) cua SGMM nen nam giua FE dong (can duoi) va POLS dong (can tren)
quietly regress lnCO2 L_lnCO2 FDI $CTRL $YDD, vce(cluster id)
di as res "POLS dong (can tren): " %6.3f _b[L_lnCO2]
quietly xtreg lnCO2 L_lnCO2 FDI $CTRL $YDD, fe vce(cluster id)
di as res "FE dong (can duoi):   " %6.3f _b[L_lnCO2]

* 8.2 Winsorize FDI 1%/99%: FEDYNDK + jackknife cho H1 va H3 (D12, D23b)
fedyn_jk H1w_FEDYNDK FDI_w $CTRL
foreach k of global IQALL {
    fedyn_jk H3w_FEDYNDK_`k' FDI_wc `k'_c FDIwx`k' $CTRL
}

* 8.3 Sai phan dau (FD): D.lnCO2 ~ D.(kiem soat) + FDI, IQk o dang muc + dummy nam, SE DK (D23c)
eststo clear
eststo FD_H1: xtscc D_lnCO2 FDI $DCTRL $YDD, lag(2)
foreach k of global IQALL {
    eststo FD_H2_`k': xtscc D_lnCO2 FDI `k' $DCTRL $YDD, lag(2)
    eststo FD_H3_`k': xtscc D_lnCO2 FDI_c `k'_c FDIx`k' $DCTRL $YDD, lag(2)
}
esttab FD_* using "$OUT/T9_FD.rtf", replace b(4) se(4) star(* 0.10 ** 0.05 *** 0.01) ///
    drop(yr* _cons) label title("Bang 9. Sai phan dau (kiem dinh vung)")

* 8.4 FE dong + xu the tuyen tinh rieng tung nuoc (FEDYNTR), SE DK (D23d)
eststo clear
eststo TR_H1: xtscc lnCO2 L_lnCO2 FDI $CTRL $YDD $TR, fe lag(2)
foreach k of global IQALL {
    eststo TR_H2_`k': xtscc lnCO2 L_lnCO2 FDI `k' $CTRL $YDD $TR, fe lag(2)
    eststo TR_H3_`k': xtscc lnCO2 L_lnCO2 FDI_c `k'_c FDIx`k' $CTRL $YDD $TR, fe lag(2)
}
esttab TR_* using "$OUT/T10_FEDYN_xuthe.rtf", replace b(4) se(4) star(* 0.10 ** 0.05 *** 0.01) ///
    drop(yr* tr* _cons) label title("Bang 10. FE dong + xu the rieng tung nuoc (kiem dinh vung)")

log close
* Ket thuc. Log: stata_out/log_FDI_CO2.smcl ; bang Word: stata_out/T*.rtf
