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
#     profile = webdriver.FirefoxProfile()
#     # We set the coordinate of where we want to be.
#     profile.set_preference("geo.wifi.uri", 'data:application/json,{"location": params, "accuracy": 100.0}')
#     # This line is necessary to avoid to prompt for geolocation authorization.
#     profile.set_preference("geo.prompt.testing", True)
    driver = webdriver.Firefox(
        options=firefoxOptions,
        service=service,
    )
    
    driver.get('https://logbook.pajak.go.id/login')
    time.sleep(3)
    driver.find_element(By.ID,'nip').send_keys(nip)
    driver.find_element(By.ID,'password').send_keys(password)
    driver.find_element(By.ID,"m_login_signin_submit").click()
    time.sleep(2)
    driver.find_element(By.ID,'btnPresensi').click()
    time.sleep(2)
    driver.get('https://logbook.pajak.go.id/Presensi')
    time.sleep(1)
    data = pd.DataFrame(columns=['Hal',':','ket'])
    tabel =driver.find_elements(By.TAG_NAME,'tr')
    for baris in tabel[2:6]:
        row = baris.find_elements_by_tag_name('td')
        row_data = [x.text for x in row]
        data.loc[len(data)] = row_data
    
    return data
    driver.close()
    driver.quit()

if __name__ == '__main__':
    st.title('Absen')
    st.caption('Data anda aman, tapi hal lain resiko ditanggung sendiri yak ')
    nip = st.text_input('NIP Pendek')
    password =st.text_input('Password')
    if st.button('Absen Klik disini ygy'):
        with st.spinner('Sedang Mencoba...'):
            hasil = selenium(nip,password)
            st.table(hasil)
            st.code("credit by gengsu07")


