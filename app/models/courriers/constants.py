COURRIERS = frozenset({"STF", '99M', "FDX", "UPS", "RPK", "DHL"})


def set_html(peso_declarado,precio_publico,precio_pakke):

    html = f"""
    <html>
      <style>
        @import url("https://fonts.googleapis.com/css?family=Open+Sans:300,400,700,800");
        body {{
          margin-top: 0px;
          margin-right: 0px;
          margin-bottom: 0px;
          margin-left: 0px;
          font-family: "Open Sans", sans-serif; 
        }}
      </style>
      <body style="color: black;">
        <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%">
          <tr>
            <td align="center" valign="top">
              <table style="margin-top:30px;">
                <tr>
                  <th style="border-bottom: solid black;">
                    <table>
                      <tr>
                        <th style="width: 65%; padding-bottom: 30px;">
                          <img src="https://lh3.googleusercontent.com/tUl4FA1kaPpr4UPQ4kGiuI_m-QrDBxFx8n2vC1ZFXP002GR5f-wqxyS4RgYetjId35usgrZmSac9">
                        </th>
                        <th style="width: 35%; text-align: start; border-left: solid black; padding:15px; padding-bottom: 30px;">
                          <span style="font-size: 45px; font-weight: 800;">CERTIFICADO DE REGALO</span style="font-size: 30px;">
                        </th>
                      </tr>
                    </table>
                  </th>
                </tr>
                <tr>
                  <th style="border-bottom: solid black;">
                    <table>
                      <tr>
                        <th style="width: 15%; display:block; padding: 15px;">
                          <label style="font-weight: 400; font-size: 20px;">ORIGEN:</label>                      
                        </th>
                        <th style="width: 45%; text-align: start; padding: 15px;">
                          <label style="font-weight: 700; font-size: 28px;">ECSE 2018</label>
                        </th>
                        <th style="width: 15%; display:block; padding: 15px;">
                          <label style="font-weight: 400; font-size: 20px;">DESTINO:</label>
                        </th>
                        <th style="width: 25%; text-align: end; padding: 15px;">
                          <label style="font-weight: 700; font-size: 28px;">74526 CUN,MX</label>
                        </th>
                      </tr>
                    </table>
                  </th>
                </tr>
                <tr>
                  <th style="border-bottom: solid black;">
                    <table>
                      <tr>
                        <th style="padding: 5px !important; text-align: start; padding: 15px;">
                          <label style="font-weight: 300; font-size: 20px;">PESO DECLARADO:</label>
                        </th>
                        <th style="padding: 5px !important; text-align: start; padding: 15px;">
                          <label style="font-weight: 700; font-size: 28px;">{peso_declarado} KG</label>
                        </th>
                      </tr>
                      <tr>
                        <th style="padding: 5px !important; text-align: start; padding: 15px;">
                          <label style="font-weight: 400; font-size: 30px;">PRECIO PUBLICO:</label>
                        </th>
                        <th style="padding: 5px !important; text-align: start; padding: 15px;">
                          <label style="font-weight: 400; font-size: 40px;">${precio_publico}</label>
                        </th>
                      </tr>
                      <tr>
                        <th style="padding: 5px !important; text-align: start; padding: 15px;">
                          <label style="font-weight: 700; font-size: 30px;">PRECIO PAKKE:</label>
                        </th>
                        <th style="padding: 5px !important; text-align: start; padding: 15px;">
                          <label style="font-weight: 700; font-size: 40px;">${precio_pakke}</label>
                        </th>
                      </tr>
                    </table>
                  </th>
                </tr>
                <tr>
                  <th style="border-bottom: solid black;">
                    <table width="1000">
                      <tr>
                        <th style="padding-top:15px;">
                          <img width="80%" src="https://lh3.googleusercontent.com/eqOjuwHWy0Hw7s1fI9oKf2LudWe1lWxkU4BREV_gXEzCv_FZG38-FtXeNVsDVqWIN92we13oBfdK">
                        </th>                    
                      </tr>
                      <tr>
                        <th style="padding:40px; padding-right: 60px; padding-left: 60px;">
                          <label style="font-size: 35px; font-weight: 700;">Ahorra <span style="font-size: 50px;">hasta un 50%</span> en tus
                            próximos envíos y obtén un descuento adicional con el siguiente código</label>
                        </th>
                      </tr>
                      <tr>
                        <th>
                          <label style="border: solid black; font-size: 40px; font-weight: 600; padding:5px;">ECSE26</label>
                        </th>
                      </tr>
                      <tr>
                        <th style="padding:40px; padding-right: 60px; padding-left: 60px;">
                          <label style="font-size: 30px; font-weight: 400;">y canjéalo en <span style="font-size: 30px; font-weight: 700;">www.pakke.mx</span></label>
                        </th>
                      </tr>
                    </table>
                  </th>
                </tr>
                <tr>
                  <th style="padding-bottom: 50px;">
                    <table width="1000">
                      <tr>
                        <th style="padding-top: 50px;">
                          <img width="80%" src="https://lh3.googleusercontent.com/PvqxLrieohD2lrq0Yf0W3FgFXIDdPRLgR3ePl9Sks31qG02lGkJyMZTCMxT9T1dswhheIZH2dGFH">
                        </th>
                      </tr>
                      <tr>
                        <th style="padding-top:25px;">
                          <p style="font-size: 25px; font-weight: 250; margin:5px !important;">Válido hasta el 05 de octubre 2018, en www.pakke.mx</p>
                          <p style="font-size: 25px; font-weight: 300; margin:0px !important;">Aplica términos y condiciones de www.pakke.mx</p>
                        </th>
                      </tr>
                    </table>
                  </th>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>"""

    return html
