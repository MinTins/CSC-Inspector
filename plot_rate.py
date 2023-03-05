
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pymysql

from config import DB_LOGIN_DATA, SITE_MONITORING_LOCATION, MONITORING_STATS



def get_abit_rate():
    conn = pymysql.connect(**DB_LOGIN_DATA)
    cursor = conn.cursor()

    cursor.execute(f'''SELECT * FROM abit_request ORDER BY date''')
    abit_rate_data = cursor.fetchall()

    conn.commit()

    return abit_rate_data



def make_graph_page(abit):

    specialities = ["Прикладна математика (113)", "<b>Приріст</b>", "Програмна інженерія (121)","Комп'ютерні науки (122)", "<b>Середній бал</b>", "Системний аналіз (124)"]
    coords =[(pos1, pos2) for pos1 in range(1,4) for pos2 in range(1,4)]

    fig = make_subplots(rows=2, cols=3,subplot_titles=specialities)

    spec_info  = {}
    spec_info["Час"] = [x[4] for x in abit]

    special = [(1,1), (1,3), (2,1), (2,3)]
    special_colors = ["#564BEB", "#EB606D", "#EB994F", "#6AEB87"]
    obj_spec = ["Прикладна математика (113)", "Програмна інженерія (121)", "Комп'ютерні науки (122)", "Системний аналіз (124)"]
    for numb, (specs, (x,y)) in enumerate(zip(obj_spec, special)):
        spec_info["Загально"] = [int(x[numb].split(";")[0]) for x in abit]
        spec_info["Приріст"]= [0] + [req_count[1] - req_count[0] for x in range(len(abit)-1)
                                        for req_count in ([int(k[numb].split(";")[0]) for k in abit[x:x+2]],)]
        spec_info["Бюджет"] = [int(x[numb].split(";")[1]) for x in abit]
        spec_info["ср.бал"] = [float(x[numb].split(";")[2]) for x in abit]

        arrange_increase = sum(spec_info["Приріст"]) / ((len(spec_info["Приріст"])-1)/2)
        future_prediction = int(abit[-1][numb].split(";")[0]) + round(arrange_increase*1)
        max_prediction = future_prediction + round(arrange_increase)

        #print(f"Середній приріст (в день) \"{specs}\": {arrange_increase:.2f} | Прогнозовано заявок: {future_prediction} - {max_prediction}")

        if numb == 0:
            fig.add_trace(go.Scatter(x=spec_info["Час"], y=spec_info["ср.бал"], text=[f"<b>{specs}</b><br>Середній бал: ~{x}" for x in spec_info["ср.бал"]],
                legendgroup="Середній бал",legendgrouptitle_text="<b>Середній бал/Приріст</b>", name=specs, line={"color": special_colors[numb]}, showlegend=True),
                row=2, col=2)

            fig.add_trace(go.Scatter(x=spec_info["Час"], y=spec_info["Приріст"], text=[f"<b>{specs}</b><br>Приріст: +{x}" for x in spec_info["Приріст"]],
                legendgroup="Приріст",legendgrouptitle_text="<b>Приріст</b>", name=specs, line={"color": special_colors[numb]}, showlegend=False),
                row=1, col=2)
        else:
            fig.add_trace(go.Scatter(x=spec_info["Час"], y=spec_info["ср.бал"], text=[f"<b>{specs}</b><br>Середній бал: ~{x}" for x in spec_info["ср.бал"]],
                legendgroup="Середній бал", name=specs, line={"color": special_colors[numb]}, showlegend=True),
                row=2, col=2)

            fig.add_trace(go.Scatter(x=spec_info["Час"], y=spec_info["Приріст"], text=[f"<b>{specs}</b><br>Приріст: +{x}" for x in spec_info["Приріст"]],
                legendgroup="Приріст", name=specs, line={"color": special_colors[numb]}, showlegend=False),
                row=1, col=2)


        fig.add_trace(go.Scatter(x=spec_info["Час"], y=spec_info["Загально"], text=[f"<b>К-ть заяв (всього):</b> [{x}]" for x in spec_info["Загально"]],
            legendgroup=specs,legendgrouptitle_text=f"<b>Спеціальності</b>", name="Загальна к-ть заяв", line={"color": "#A487FF"}, showlegend=numb==0),
             row=x, col=y)

        fig.add_trace(go.Scatter(x=spec_info["Час"], y=spec_info["Бюджет"], text=[f"<b>К-ть заяв на бюджет:</b> [{x}]<br>(з допущених)" for x in spec_info["Бюджет"]],
            legendgroup=specs, name="На бюджет (з допущених)", line={"color": "#E3B027"}, showlegend=numb==0),
             row=x, col=y)

        fig.add_trace(go.Scatter(x=spec_info["Час"], y=spec_info["Приріст"], text=[f"<b>Приріст:</b> +{x}" for x in spec_info["Приріст"]],
            legendgroup=specs, name="Приріст", line={"color": "#6CE3E6"}, showlegend=numb==0),
             row=x, col=y)


    fig.update_layout(width=1479, height=707, title="<b>Моніторинг поданих заявок у часі</b>", showlegend=True)
    #fig.write_image(MONITORING_STATS)
    fig.write_html(SITE_MONITORING_LOCATION)


def update_monitoring_page():
    abit = get_abit_rate()
    make_graph_page(abit)


if __name__ == "__main__":
    update_monitoring_page()