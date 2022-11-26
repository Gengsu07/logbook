import streamlit as st
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

def selenium(nip,password):
    params = {
        "latitude": -6.181564761467654,
        "longitude": 106.83369439912856,
        "accuracy": 100 }

    firefoxOptions = Options()
    firefoxOptions.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(
        options=firefoxOptions,
        service=service,
    )
    driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
    driver.get('https://logbook.pajak.go.id/login')
    time.sleep(2)
    driver.find_element_by_xpath('//input[@id="nip"]').send_keys(nip)
    driver.find_element_by_xpath('//input[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//button[@name="m_login_signin_submit"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//button[@id="btnPresensi"]').click()
    time.sleep(2)
    driver.get('https://logbook.pajak.go.id/Presensi')
    time.sleep(1)
    data = pd.DataFrame(columns=['Hal',':','ket'])
    tabel =driver.find_elements_by_tag_name('tr')
    for baris in tabel[2:6]:
        row = baris.find_elements_by_tag_name('td')
        row_data = [x.text for x in row]
        data.loc[len(data)] = row_data
    driver.close()
    driver.quit()
    return data

if __name__ = '__main__':
    st.title('Absen')
    st.caption('Data anda aman, tapi hal lain resiko ditanggung sendiri yak ')
    nip = st.text_input('NIP Pendek')
    password =st.text_input('Password')
    if st.button('Absen Klik disini ygy'):
        with st.spinner('Sedang Mencoba...'):
            hasil = selenium(nip,password)
            st.table(hasil)
            st.code("credit by gengsu07")


