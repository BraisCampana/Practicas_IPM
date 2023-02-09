import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:tarea3/main.dart';
import 'server_calls.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:intl/date_symbol_data_local.dart' as dateformat;
import 'package:conveter/const.dart';
import 'package:conveter/Temperature.dart';
import 'package:conveter/Conveter.dart';

class ListEvento extends StatefulWidget {
  ListEvento({Key? key, required this.value, required this.list})
      : super(key: key);

  final bool value;
  final List<dynamic> list;

  @override
  State<ListEvento> createState() => _ListEvento();
}

class _ListEvento extends State<ListEvento> {
  late dateChangerEvento dateChangeEvent;
  late ServerCalls database;
  late List<dynamic> list;

  getTemperature(double temperature) {
    CConveter conveter = CConveter(
        value: temperature, cType: CType.Temperature, from: Unit.c, to: Unit.f);
    return conveter.convert().floor().toString();
  }

  @override
  void initState() {
    super.initState();
    dateChangeEvent = context.read<dateChangerEvento>();
    database = ServerCalls();
    list = widget.list;
    dateformat.initializeDateFormatting('en', null);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.listaEvento),
        elevation: 0,
        centerTitle: true,
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 20.0),
            child: GestureDetector(
              onTap: () {
                _buildPopupDialogEvento(context, list);
              },
              child: const Icon(Icons.info_outline),
            ),
          )
        ],
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Row(mainAxisAlignment: MainAxisAlignment.start, children: [
            Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [dateChangeEvent.changeFecha(context)],
            ),
            const SizedBox(width: 20),
            IconButton(
                iconSize: 35.0,
                icon: const Icon(Icons.filter_alt_rounded),
                onPressed: () async {
                  if (dateChangeEvent.getFechaEntrada() == "" ||
                      dateChangeEvent.getFechaSalida() == "") {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                          content:
                              Text(AppLocalizations.of(context)!.nullDate)),
                    );
                  } else if (DateFormat("dd/MM/yyyy")
                      .parse(dateChangeEvent.getFechaEntrada())
                      .isBefore(DateFormat("dd/MM/yyyy")
                          .parse(dateChangeEvent.getFechaSalida()))) {
                    String timestampEntrada = getTimestampEntrada();
                    String timestampSalida = getTimestampSalida();
                    Uri url = Uri.parse(
                        "http://10.0.2.2:8080/api/rest/facility_access_log/130/daterange");
                    var data = {
                      "startdate": timestampEntrada,
                      "enddate": timestampSalida
                    };
                    Map<String, dynamic> responseJson =
                        await database.getListEventoRange(data, url, context);
                    setState(() {
                      list = responseJson["access_log"];
                    });
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                          content: Text(AppLocalizations.of(context)!.badDate)),
                    );
                  }
                })
          ]),
          Expanded(
              child: SizedBox(
                  height: MediaQuery.of(context).size.height * 0.76,
                  child: ListView.builder(
                      itemCount: list.length,
                      itemBuilder: (BuildContext context, int index) {
                        return Card(
                            child: ListTile(
                          leading: const Icon(Icons.account_circle, size: 50.0),
                          title: Text(
                              list[index]['user']['name'] +
                                  " " +
                                  list[index]['user']['surname'],
                              style: const TextStyle(fontSize: 20.0)),
                          subtitle: Text(list[index]['user']['phone'] +
                              "\n" +
                              list[index]['user']['email']),
                          isThreeLine: true,
                          trailing: IconButton(
                              iconSize: 30.0,
                              icon: const Icon(Icons.info_outlined),
                              onPressed: () {
                                _buildPopupDialog(context, list, index);
                              }),
                        ));
                      })))
        ],
      ),
    );
  }

  Future<dynamic> _buildPopupDialogEvento(
      BuildContext context, List<dynamic> list) {
    return showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            backgroundColor: Colors.amber[100],
            title: Text(AppLocalizations.of(context)!.informacionEvento,
                textAlign: TextAlign.center),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(AppLocalizations.of(context)!.visitasEvento +
                    ": " +
                    database.getPeopleVisit(list)),
                Text(AppLocalizations.of(context)!.actualEvento +
                    ": " +
                    database.getPeopleInside(list).toString()),
              ],
            ),
            actions: [
              MaterialButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                textColor: Theme.of(context).primaryColor,
                child: Text(AppLocalizations.of(context)!.cerrar),
              )
            ],
          );
        });
  }

  Future<dynamic> _buildPopupDialog(
      BuildContext context, List<dynamic> userList, int index) {
    String vacunado = userList[index]['user']['is_vaccinated']
        ? AppLocalizations.of(context)!.si
        : "No";
    String type = "";
    if (userList[index]['type'] == "IN") {
      type = "Entrada";
    } else {
      type = "Salida";
    }
    String measure = "ºC";
    String temperatura = userList[index]['temperature'];
    if (Localizations.localeOf(context).toLanguageTag() == "en" ||
        Localizations.localeOf(context).toLanguageTag() == "fr") {
      measure = "ºF";
      temperatura =
          getTemperature(double.parse(userList[index]['temperature']));
    }
    String aux =
        userList[index]['timestamp'].toString().split("T")[0]; // 2021-12-25
    DateTime formato = DateFormat(
            "yyyy-MM-dd", Localizations.localeOf(context).toLanguageTag())
        .parse(aux);
    String hora =
        userList[index]['timestamp'].toString().split("T")[1].split("+")[0];
    return showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            backgroundColor: Colors.amber[100],
            title: Text(AppLocalizations.of(context)!.infoUser,
                textAlign: TextAlign.center),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("UUID: " + userList[index]['user']['uuid']),
                Text(AppLocalizations.of(context)!.nombre +
                    ": " +
                    userList[index]['user']['name']),
                Text(AppLocalizations.of(context)!.apellido +
                    ": " +
                    userList[index]['user']['surname']),
                Text(AppLocalizations.of(context)!.telefono +
                    ": " +
                    userList[index]['user']['phone']),
                Text(AppLocalizations.of(context)!.email +
                    ": " +
                    userList[index]['user']['email']),
                Text(AppLocalizations.of(context)!.vacunado + ": " + vacunado),
                Text(AppLocalizations.of(context)!.temperatura +
                    ": " +
                    temperatura +
                    measure),
                Text(AppLocalizations.of(context)!.fecha +
                    ": " +
                    DateFormat.yMd(
                            Localizations.localeOf(context).toLanguageTag())
                        .format(formato)),
                Text(AppLocalizations.of(context)!.hora + ": " + hora),
                Text(AppLocalizations.of(context)!.tipo + ": " + type)
              ],
            ),
            actions: [
              MaterialButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                textColor: Theme.of(context).primaryColor,
                child: Text(AppLocalizations.of(context)!.cerrar),
              )
            ],
          );
        });
  }

  String getTimestampEntrada() {
    String timestamp, aux, fecha;
    timestamp = aux = fecha = "";
    aux = dateChangeEvent.getFechaEntrada().replaceAll("/", "-"); //13-12-2021
    fecha = aux.split("-")[2] +
        "-" +
        aux.split("-")[1] +
        "-" +
        aux.split("-")[0]; //2021-12-13
    if (Localizations.localeOf(context).toLanguageTag() == "en") {
      fecha = aux.split("-")[2] +
          "-" +
          aux.split("-")[0] +
          "-" +
          aux.split("-")[1]; //2021-12-13
    }
    timestamp = fecha + "T";
    if (dateChangeEvent.getHoraEntrada() == "") {
      timestamp = timestamp + "00:00:00+00:000";
    } else {
      timestamp = timestamp + dateChangeEvent.getHoraEntrada() + "+00:000";
    }
    //startdate for calling database
    return timestamp;
  }

  String getTimestampSalida() {
    String timestamp, aux, fecha;
    timestamp = aux = fecha = "";
    aux = dateChangeEvent.getFechaSalida().replaceAll("/", "-"); //13-12-2021
    fecha = aux.split("-")[2] +
        "-" +
        aux.split("-")[1] +
        "-" +
        aux.split("-")[0]; //2021-12-13
    if (Localizations.localeOf(context).toLanguageTag() == "en") {
      fecha = aux.split("-")[2] +
          "-" +
          aux.split("-")[0] +
          "-" +
          aux.split("-")[1]; //2021-12-13
    }
    timestamp = fecha + "T";
    if (dateChangeEvent.getHoraSalida() == "") {
      timestamp = timestamp + "00:00:00+00:000";
    } else {
      timestamp = timestamp + dateChangeEvent.getHoraSalida() + "+00:000";
    } //startdate for calling database
    return timestamp;
  }
}
