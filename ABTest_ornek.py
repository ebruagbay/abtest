# İş Problemi : # Facebook kısa süre önce mevcut maximum bidding adı verilen teklif verme türüne alternatif olarak
                # yeni bir teklif türü olan average bidding’i tanıttı.
                # Müşterilerimizden biri olan ebru.com, bu yeni özelliği test etmeye karar verdi ve average
                # bidding'in, maximum bidding'den daha fazla DÖNÜŞÜM getirip getirmediğini anlamak için bir A/B testi
                # yapmak istiyor.
# Facebook sayfasında ebru.com müşterisi reklamlarını hangi servis kullanarak vermeli (max bidding or avg bidding)?

# Müşterinin web site bilgilerini içeren veri setinde kullancıların gördükleri (Impression) ve tıkladıkları reklam
    # sayıları (Click) gibi bilgiler ve kazanç bilgileri (Earning) yer alıyor.

# control grubu verileri; eski hizmet olan maximum bidding ile yönetilen reklamlara ait
# test grubu verileri; yeni hizmet olan average bidding ile yönetilen reklamların deneme süresine ait


import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control=pd.read_excel("Ders Notları ve Ödevler/HAFTA_05/Ders Notları/ab_testing.xlsx", sheet_name="Control Group")
df_control.head(20)

df_test=pd.read_excel("Ders Notları ve Ödevler/HAFTA_05/Ders Notları/ab_testing.xlsx", sheet_name="Test Group")
df_test.head(20)

df_control["Earning"].describe() # median=1975.160
df_test["Earning"].describe()  # median=2544.666

# Kazanç ortalamaları arasında gözle görülür bir fark olmasına rağmen istatistiki olarak da gösterelim niyetindeyiz :)

# GÖREV-1 : A/B testinin hipotezini tanımlayınız.

# Ho : average bidding dönüşümü = maximum bidding dönüşümü
        # (iki farklı teklif yöntemine göre kazançlar arasında istatistiki olarak anlamsal bir farklılık yoktur)
# H1: average bidding dönüşümü != maximum bidding dönüşümü
        # (iki farklı teklif yöntemine göre kazançlar arasında istatistiki olarak anlamsal bir farklılık vardır)

# GÖREV-2 : Çıkan test sonuçlarının istatistiksel olarak anlamlı olup olmadığını yorumlayınız.

# VARSAYIMLARIN TEST EDİLMESİ

# p-value <  0.05 -> Ho RED.
# p-value >  0.05 -> Ho REDDEDILEMEZ.

# Normallik Varsayımı (Ho: Normal dağılım varsayımı sağlanmaktadır.)
test_stat, pvalue = shapiro(df_control["Earning"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p>0.05 Ho reddedilemez

test_stat, pvalue = shapiro(df_test["Earning"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p>0.05 Ho reddedilemez
# Normallik varsayımı sağlanmaktadır.

# Varyans Homojenligi Varsayımı (Ho: Varyanslar homojendir)
test_stat, pvalue = levene(df_control["Earning"],df_test["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p>0.05 Ho reddedilemez
# Varyanslar homojendir.

# GÖREV-3 : Hangi testleri kullandınız? Neden.
# Varsayımlar sağlandığı için PARAMETRİK test (Bağımsız İki Örneklem T Testi) kullanıldı.
test_stat, pvalue = ttest_ind(df_control["Earning"],df_test["Earning"], equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p<0.05 Ho reddedilir. İst. ol. anl. fark vardır.

# GÖREV-4 : Görev 2’de verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?

# Eski teklif üzerinden elde ettiğiniz kazançların ortalaması ile yeni teklif üzerinden toplanan sınırlı sayıdaki test
# verilerindeki kazançların ortalaması istatistiki bazı yöntemler ile karşılaştırılmıştır ve istatistiki olarak aralarında
# anlamlı bir fark bulunmuştur. Yeni teklif ile kazançlarınızın artacağını ön görüyoruz.

# EXTRA

# İki Örneklem Oran Testi
    # Eski teklif ile reklamların dönüşüm oranı ve yeni teklif ile elde edilen dönüşüm oranlarının
    # karşılaştırılması amaçlanmaktadır.

df_control["conv_rate"]=df_control["Click"]/df_control["Impression"]
df_control.head()
df_control["conv_rate"].mean() # 0.0536

df_test["conv_rate"]=df_test["Click"]/df_test["Impression"]
df_test.head()
df_test["conv_rate"].mean() # 0.03417

# Dönüşüm oranı ortalaması, eski teklif ile verilen reklamlarda 0.0536 iken yeni teklif ile verilen reklamlarda 0.0342..
# Fark gözle görülebilir denilebilir,ancak istatistiki olarak da kontrol sağlayalım.

# basari_sayisi : Click parametresi
# gozlem_sayisi : Impression parametresi

df_control["type"]="control"
df_test["type"]="test"

df_merge=pd.concat([df_control,df_test],axis=0,ignore_index=True)
df_merge.head()

# Başarı Sayısı
control_succ_count = df_merge.loc[df_merge["type"] == "control", "Click"].sum() # 204026.29490309
test_succ_count = df_merge.loc[df_merge["type"] == "test", "Click"].sum() # 158701.99043224

# Gözlem sayısı
control_obv_count=df_merge.loc[df_merge["type"] == "control", "Impression"].sum() # 4068457.96270789
test_obv_count=df_merge.loc[df_merge["type"] == "test", "Impression"].sum() # 4820496.47030138

test_stat, pvalue = proportions_ztest(count=[control_succ_count,test_succ_count],
                                      nobs=[control_obv_count,test_obv_count])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p<0.05 -> Ho reddedilir.. Fark vardır demektir...

# Eski teklif ile dönüşüm oranları daha yüksek bulunmuştur. Bunun sebebi olarak yeni sistemin test edilme süresinin
# kısalığı olarak değerlendirebiliriz.

# Dönüşüm oranından (reklamı görüp ilgili siteye gitmek için tıklayanların oranından) ziyade satın alma oranı (siteye
# gitmek için tıklayıp satın alanların oranı) kazancı etkileyeceğinden ötürü satın alma oranları aşağıda karşılaştırılmıştır.

df_control.sort_values("Earning", ascending=False)
#     Impression      Click  Purchase    Earning  conv_rate     type
# 31  92044.50011 4667.20523 729.36526 2497.29522    0.05071  control
# 9   79498.24866 6653.84552 470.50137 2456.30424    0.08370  control
# 0   82529.45927 6090.07732 665.21125 2311.27714    0.07379  control
# 35 132064.21900 3747.15754 551.07241 2256.97559    0.02837  control
# 38 101997.49410 4736.35337 474.61354 2254.56383    0.04644  control

df_test.sort_values("Earning", ascending=False)
#     Impression      Click  Purchase    Earning  conv_rate  type
# 12 157681.15975 4468.26679 701.58760 3171.48971    0.02834  test
# 39 102257.45409 4800.06832 521.31073 2967.51839    0.04694  test
# 1  134775.94336 3635.08242 834.05429 2929.40582    0.02697  test
# 21  97507.36685 4119.21862 670.52139 2832.58467    0.04225  test
# 14 119877.96005 3622.93635 689.15574 2811.50273    0.03022  test

df_control["purch_rate"]=df_control["Purchase"]/df_control["Click"]
df_control.head()
df_control["purch_rate"].mean() #0.1159

df_test["purch_rate"]=df_test["Purchase"]/df_test["Click"]
df_test.head()
df_test["purch_rate"].mean() # 0.15657

# Reklamı görüp web sitesine gitmek için tıklayanların oranı eski teklif üzerinden daha çok olsa da,
# satın alma miktarının yeni teklif ile arttığını söyleyebiliriz. Test etmeye gerek duyulmamıştır.