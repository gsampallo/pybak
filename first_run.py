import Models

import datetime

import BD

def run():
    # d = Door('Puerta',1,1)
    # DB.session.add(d)
    # DB.session.commit()


    #camara = Camara(camara_name = 'Cam1',camara_url='rtsp://192.168.1.10:554/user=admin&password=&channel=1&stream=0.sdp?')
    # DB.session.add(camara)
    # DB.session.commit()
    #vf = VideoFile(date_time = datetime.datetime.now(),door_id = 1,filename='archivo.mp4')
    #DB.session.add(vf)
    #DB.session.commit()

    pass

if __name__ == '__main__':
    BD.Base.metadata.create_all(BD.engine)
    run()

