import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'package:string_validator/string_validator.dart';
import 'package:tarea3/main.dart';
import 'multiple_users.dart';
import 'server_calls.dart';
import 'package:provider/provider.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:conveter/const.dart';
import 'package:conveter/Temperature.dart';
import 'package:conveter/Conveter.dart';

class AddQRManualPage extends StatefulWidget {
  AddQRManualPage(
      {Key? key,
      required this.manual,
      required this.name,
      required this.surname,
      required this.uuid})
      : super(key: key);

  final bool manual;
  final String name;
  final String surname;
  final String uuid;

  @override
  State<AddQRManualPage> createState() => _AddQRManualPage();
}

class _AddQRManualPage extends State<AddQRManualPage> {
  late bool value;
  late final _formKey; //necesario para controlar validación en los entrys
  late TextEditingController _nombre;
  late TextEditingController _apellido;
  late TextEditingController _temperatura;
  late TextEditingController _fecha;
  late TextEditingController _hora;
  late ServerCalls database;
  var dateChange;
  var noFecha;
  var noHora;
  String _qr = "";
  String measure = "ºC";

  @override
  void initState() {
    super.initState();

    dateChange = context.read<dateChanger>();
    database = ServerCalls();
    _nombre = TextEditingController();
    _apellido = TextEditingController();
    _temperatura = TextEditingController();
    _fecha = TextEditingController();
    _hora = TextEditingController();
    _formKey = GlobalKey<FormState>();
    value = false;
    noFecha = false;
    noHora = false;
  }

  @override
  Widget build(BuildContext context) {
    if (Localizations.localeOf(context).toLanguageTag() == "en" ||
        Localizations.localeOf(context).toLanguageTag() == "fr") {
      measure = "ºF";
    }
    return Scaffold(
        appBar: AppBar(
            title: Text(AppLocalizations.of(context)!.anotarES),
            centerTitle: true),
        resizeToAvoidBottomInset: true,
        body: Form(
            key: _formKey,
            child: SingleChildScrollView(
                child: Center(
                    child: Column(
              children: [
                Padding(
                    padding: EdgeInsets.only(
                        bottom: MediaQuery.of(context).size.height * 0.05),
                    child: Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: [
                          Checkbox(
                              activeColor: Colors.blue,
                              value: value,
                              onChanged: (val) {
                                setState(() {
                                  value = !value;
                                });
                              }),
                          Text(AppLocalizations.of(context)!.cambiarFecha,
                              style: const TextStyle(fontSize: 15.0)),
                        ])),
                Padding(
                    padding: EdgeInsets.only(
                        bottom: MediaQuery.of(context).size.height * 0.05),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(AppLocalizations.of(context)!.fecha,
                            style: const TextStyle(fontSize: 20.0)),
                        value
                            ? dateChange.changeFecha(context)
                            : SizedBox(
                                width: MediaQuery.of(context).size.width * 0.25,
                                child: TextFormField(
                                  controller: _fecha
                                    ..text = DateFormat.yMd(
                                            Localizations.localeOf(context)
                                                .toLanguageTag())
                                        .format(DateTime.now()),
                                  enabled: false,
                                ))
                      ],
                    )),
                Padding(
                    padding: EdgeInsets.only(
                        bottom: MediaQuery.of(context).size.height * 0.05),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(AppLocalizations.of(context)!.hora,
                            style: const TextStyle(fontSize: 20.0)),
                        value
                            ? dateChange.changeHora(context)
                            : SizedBox(
                                width: MediaQuery.of(context).size.width * 0.25,
                                child: TextFormField(
                                  controller: _hora
                                    ..text = DateTime.now().hour.toString() +
                                        ":" +
                                        DateTime.now().minute.toString() +
                                        ":" +
                                        DateTime.now().second.toString(),
                                  enabled: false,
                                ))
                      ],
                    )),
                Padding(
                    padding: EdgeInsets.only(
                        bottom: MediaQuery.of(context).size.height * 0.05),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(AppLocalizations.of(context)!.nombre,
                            style: const TextStyle(fontSize: 20.0)),
                        widget.manual
                            ? SizedBox(
                                width: MediaQuery.of(context).size.width * 0.65,
                                child: TextFormField(
                                    controller: _nombre,
                                    decoration: const InputDecoration(
                                      border: OutlineInputBorder(
                                          borderSide: BorderSide(
                                              color: Colors.red, width: 2.0)),
                                      hintText: "Ex: David",
                                    ),
                                    validator: (value) {
                                      if (value == null ||
                                          value.isEmpty ||
                                          !isAlpha(value.trim())) {
                                        return AppLocalizations.of(context)!
                                            .entryNombre;
                                      }
                                      return null;
                                    }))
                            : Text(widget.name,
                                style: const TextStyle(fontSize: 20.0))
                      ],
                    )),
                Padding(
                    padding: EdgeInsets.only(
                        bottom: MediaQuery.of(context).size.height * 0.05),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(AppLocalizations.of(context)!.apellido,
                            style: const TextStyle(fontSize: 20.0)),
                        widget.manual
                            ? SizedBox(
                                width: MediaQuery.of(context).size.width * 0.65,
                                child: TextFormField(
                                    controller: _apellido,
                                    decoration: const InputDecoration(
                                        border: OutlineInputBorder(
                                            borderSide: BorderSide(
                                                color: Colors.red, width: 2.0)),
                                        hintText: "Ex: Gayoso"),
                                    validator: (value) {
                                      if (value == null ||
                                          value.isEmpty ||
                                          !isAlpha(value.trim())) {
                                        return AppLocalizations.of(context)!
                                            .entryApellido;
                                      }
                                      return null;
                                    }))
                            : Text(widget.surname,
                                style: const TextStyle(fontSize: 20.0))
                      ],
                    )),
                Padding(
                    padding: EdgeInsets.only(
                        bottom: MediaQuery.of(context).size.height * 0.05),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(AppLocalizations.of(context)!.temperatura,
                            style: const TextStyle(fontSize: 20.0)),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.65,
                          child: TextFormField(
                              controller: _temperatura,
                              decoration: InputDecoration(
                                border: const OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.red, width: 2.0)),
                                hintText: "Ex: 39" + measure,
                              ),
                              validator: (value) {
                                if (value == null ||
                                    value.isEmpty ||
                                    !isNumeric(value)) {
                                  return AppLocalizations.of(context)!
                                      .entryTemperatura;
                                }
                                return null;
                              },
                              keyboardType: TextInputType.number,
                              inputFormatters: <TextInputFormatter>[
                                FilteringTextInputFormatter.digitsOnly
                              ]),
                        )
                      ],
                    )),
              ],
            )))),
        floatingActionButton: FloatingActionButton(
            onPressed: () async {
              if (value &&
                  dateChange.getTextFecha() == "" &&
                  dateChange.getTextHora() == "") {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                      content: Text(AppLocalizations.of(context)!.noHoraFecha)),
                );
                noFecha = true;
                noHora = true;
              } else if (value && dateChange.getTextFecha() == "") {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                      content: Text(AppLocalizations.of(context)!.noFecha)),
                );
                noFecha = true;
              } else if (value && dateChange.getTextHora() == "") {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(AppLocalizations.of(context)!.noHora)),
                );
                noHora = true;
              }
              if (_formKey.currentState!.validate()) {
                String temperatura = "";
                if (measure == "ºF") {
                  temperatura = getTemperature(double.parse(_temperatura.text));
                } else {
                  temperatura = _temperatura.text;
                }
                if (!widget.manual && !noFecha && !noHora) {
                  var userList = [
                    {"uuid": widget.uuid}
                  ];
                  database.postAccess(
                      userList, 0, temperatura, getTimestamp(), context, true);
                } else if (!noFecha && !noHora) {
                  try {
                    var response = await database.getUser(
                        _nombre.text.trim(), _apellido.text.trim());
                    Map<String, dynamic> responseJson =
                        json.decode(response.body);
                    String timestamp = getTimestamp();
                    List userList = responseJson[
                        "users"]; // lista de personas con ese nombre
                    if (userList.length > 1) {
                      Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) => MultipleUsers(
                              list: userList,
                              temperature: temperatura,
                              timestamp:
                                  timestamp))); // --> nueva ventana con lista
                    } else if (userList.length == 1) {
                      database.postAccess(
                          userList, 0, temperatura, timestamp, context, false);
                    } else if (userList.isEmpty) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                            content: Text(
                                AppLocalizations.of(context)!.userNotFound)),
                      );
                    }
                  } on Exception catch (_) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                          content:
                              Text(AppLocalizations.of(context)!.noServidor)),
                    );
                  }
                }
              }
            },
            child: const Icon(Icons.check)));
  }

  String getTimestamp() {
    String timestamp, aux, fecha;
    timestamp = aux = fecha = "";
    if (value) {
      aux = dateChange.getTextFecha().replaceAll("/", "-"); // 13-12-2021
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
      timestamp = fecha + "T" + dateChange.getTextHora() + ":00+00:00";
    } else {
      aux = _fecha.text.replaceAll("/", "-"); // 13-12-2021
      fecha =
          aux.split("-")[2] + "-" + aux.split("-")[1] + "-" + aux.split("-")[0];
      if (Localizations.localeOf(context).toLanguageTag() == "en") {
        fecha = aux.split("-")[2] +
            "-" +
            aux.split("-")[0] +
            "-" +
            aux.split("-")[1];
      }
      timestamp = fecha + "T" + _hora.text + "+00:00";
    }
    return timestamp;
  }

  getTemperature(double temperature) {
    CConveter conveter = CConveter(
        value: temperature, cType: CType.Temperature, from: Unit.f, to: Unit.c);
    return conveter.convert().floor().toString();
  }
}
