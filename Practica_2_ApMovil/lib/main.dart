// @dart=2.9

import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:intl/date_symbol_data_file.dart';
import 'package:intl/intl.dart';
import 'lista_evento.dart';
import 'add_manual_qr.dart';
import 'package:provider/provider.dart';
import 'server_calls.dart';
import 'package:file_picker/file_picker.dart';
import 'package:qr_code_tools/qr_code_tools.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:intl/date_symbol_data_local.dart' as dateformat;

class dateChanger with ChangeNotifier {
  TextEditingController _controllerFecha = TextEditingController();
  TextEditingController _controllerHora = TextEditingController();

  Widget changeFecha(context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
            width: 150,
            child: TextField(
              controller: _controllerFecha,
              enabled: false,
            )),
        IconButton(
          icon: const Icon(Icons.calendar_today),
          onPressed: () {
            showDatePicker(
                context: context,
                initialDate: DateTime(2021, 10),
                firstDate: DateTime(2021, 10),
                lastDate: DateTime(2030, 12),
                builder: (context, picker) {
                  return Theme(
                    data: ThemeData.dark().copyWith(
                      colorScheme: const ColorScheme.dark(
                        primary: Colors.blue,
                        onPrimary: Colors.white,
                        surface: Colors.blue,
                        onSurface: Colors.black,
                      ),
                      dialogBackgroundColor: Colors.white,
                    ),
                    child: picker,
                  );
                }).then((selectedDate) {
              if (selectedDate != null) {
                String myLocale =
                    Localizations.localeOf(context).toLanguageTag();
                String date =
                    DateFormat.yMd(myLocale).format(selectedDate).toString();
                _controllerFecha.text = date;
                notifyListeners();
              }
            });
          },
        )
      ],
    );
  }

  String getTextFecha() {
    return _controllerFecha.text;
  }

  Widget changeHora(context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
            width: 150,
            child: TextField(
              controller: _controllerHora,
              enabled: false,
            )),
        IconButton(
          icon: const Icon(Icons.alarm),
          onPressed: () {
            showTimePicker(
                initialTime: TimeOfDay(
                    hour: TimeOfDay.now().hour, minute: TimeOfDay.now().minute),
                context: context,
                builder: (context, picker) {
                  return MediaQuery(
                      data: MediaQuery.of(context)
                          .copyWith(alwaysUse24HourFormat: true),
                      child: Theme(
                        data: ThemeData.dark().copyWith(
                          colorScheme: const ColorScheme.dark(
                            primary: Colors.deepPurple,
                            onPrimary: Colors.white,
                            surface: Colors.pink,
                            onSurface: Colors.yellow,
                          ),
                          dialogBackgroundColor: Colors.green[900],
                        ),
                        child: picker,
                      ));
                }).then((selectedTime) {
              if (selectedTime != null) {
                String time = selectedTime.hour.toString() +
                    ":" +
                    selectedTime.minute.toString();
                _controllerHora.text = time;
                notifyListeners();
              }
            });
          },
        ),
      ],
    );
  }

  String getTextHora() {
    return _controllerHora.text;
  }
}

class dateChangerEvento with ChangeNotifier {
  TextEditingController controllerEntrada = TextEditingController();
  TextEditingController controllerSalida = TextEditingController();
  TextEditingController controllerHoraEntrada = TextEditingController();
  TextEditingController controllerHoraSalida = TextEditingController();

  Widget changeFecha(context) {
    //adaptar orientation (portrait --> vertical)
    if (MediaQuery.of(context).orientation == Orientation.landscape) {
      return Column(mainAxisAlignment: MainAxisAlignment.start, children: [
        Row(mainAxisAlignment: MainAxisAlignment.start, children: [
          Text(AppLocalizations.of(context).initialDate),
          SizedBox(
              width: MediaQuery.of(context).size.width * 0.30,
              child: TextField(
                controller: controllerEntrada,
                enabled: false,
              )),
          IconButton(
            icon: const Icon(Icons.calendar_today),
            onPressed: () {
              showDatePicker(
                  context: context,
                  initialDate: DateTime(2021, 10),
                  firstDate: DateTime(2021, 10),
                  lastDate: DateTime(2022, 12),
                  builder: (context, picker) {
                    return Theme(
                      data: ThemeData.dark().copyWith(
                        colorScheme: const ColorScheme.dark(
                          primary: Colors.blue,
                          onPrimary: Colors.white,
                          surface: Colors.blue,
                          onSurface: Colors.black,
                        ),
                        dialogBackgroundColor: Colors.white,
                      ),
                      child: picker,
                    );
                  }).then((selectedDate) {
                if (selectedDate != null) {
                  String myLocale =
                      Localizations.localeOf(context).toLanguageTag();
                  String date =
                      DateFormat.yMd(myLocale).format(selectedDate).toString();
                  controllerEntrada.text = date;
                  notifyListeners();
                }
              });
            },
          ),
          Text(AppLocalizations.of(context).initialHour),
          SizedBox(
              width: MediaQuery.of(context).size.width * 0.30,
              child: TextField(
                controller: controllerHoraEntrada,
                enabled: false,
              )),
          IconButton(
            icon: const Icon(Icons.alarm),
            onPressed: () {
              showTimePicker(
                  initialTime: TimeOfDay(
                      hour: TimeOfDay.now().hour,
                      minute: TimeOfDay.now().minute),
                  context: context,
                  builder: (context, picker) {
                    return MediaQuery(
                        data: MediaQuery.of(context)
                            .copyWith(alwaysUse24HourFormat: true),
                        child: Theme(
                          data: ThemeData.dark().copyWith(
                            colorScheme: const ColorScheme.dark(
                              primary: Colors.deepPurple,
                              onPrimary: Colors.white,
                              surface: Colors.pink,
                              onSurface: Colors.yellow,
                            ),
                            dialogBackgroundColor: Colors.green[900],
                          ),
                          child: picker,
                        ));
                  }).then((selectedTime) {
                if (selectedTime != null) {
                  String time = selectedTime.hour.toString() +
                      ":" +
                      selectedTime.minute.toString();
                  controllerHoraEntrada.text = time;
                  notifyListeners();
                }
              });
            },
          )
        ]),
        Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Text(AppLocalizations.of(context).finalDate),
            SizedBox(
                width: MediaQuery.of(context).size.width * 0.30,
                child: TextField(
                  controller: controllerSalida,
                  enabled: false,
                )),
            IconButton(
              icon: const Icon(Icons.calendar_today),
              onPressed: () {
                showDatePicker(
                    context: context,
                    initialDate: DateTime(2021, 10),
                    firstDate: DateTime(2021, 10),
                    lastDate: DateTime(2022, 12),
                    builder: (context, picker) {
                      return Theme(
                        data: ThemeData.dark().copyWith(
                          colorScheme: const ColorScheme.dark(
                            primary: Colors.blue,
                            onPrimary: Colors.white,
                            surface: Colors.blue,
                            onSurface: Colors.black,
                          ),
                          dialogBackgroundColor: Colors.white,
                        ),
                        child: picker,
                      );
                    }).then((selectedDate) {
                  if (selectedDate != null) {
                    String myLocale =
                        Localizations.localeOf(context).toLanguageTag();
                    String date = DateFormat.yMd(myLocale)
                        .format(selectedDate)
                        .toString();
                    controllerSalida.text = date;
                    notifyListeners();
                  }
                });
              },
            ),
            Text(AppLocalizations.of(context).finalHour),
            SizedBox(
                width: MediaQuery.of(context).size.width * 0.30,
                child: TextField(
                  controller: controllerHoraSalida,
                  enabled: false,
                )),
            IconButton(
              icon: const Icon(Icons.alarm),
              onPressed: () {
                showTimePicker(
                    initialTime: TimeOfDay(
                        hour: TimeOfDay.now().hour,
                        minute: TimeOfDay.now().minute),
                    context: context,
                    builder: (context, picker) {
                      return MediaQuery(
                          data: MediaQuery.of(context)
                              .copyWith(alwaysUse24HourFormat: true),
                          child: Theme(
                            data: ThemeData.dark().copyWith(
                              colorScheme: const ColorScheme.dark(
                                primary: Colors.deepPurple,
                                onPrimary: Colors.white,
                                surface: Colors.pink,
                                onSurface: Colors.yellow,
                              ),
                              dialogBackgroundColor: Colors.green[900],
                            ),
                            child: picker,
                          ));
                    }).then((selectedTime) {
                  if (selectedTime != null) {
                    String time = selectedTime.hour.toString() +
                        ":" +
                        selectedTime.minute.toString();
                    controllerHoraSalida.text = time;
                    notifyListeners();
                  }
                });
              },
            )
          ],
        ),
      ]);
    } else {
      return Column(children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(AppLocalizations.of(context).initialDate),
            SizedBox(width: MediaQuery.of(context).size.width * 0.10),
            SizedBox(
                width: MediaQuery.of(context).size.width * 0.30,
                child: TextField(
                  controller: controllerEntrada,
                  enabled: false,
                )),
            IconButton(
              icon: const Icon(Icons.calendar_today),
              onPressed: () {
                showDatePicker(
                    context: context,
                    initialDate: DateTime(2021, 10),
                    firstDate: DateTime(2021, 10),
                    lastDate: DateTime(2022, 12),
                    builder: (context, picker) {
                      return Theme(
                        data: ThemeData.dark().copyWith(
                          colorScheme: const ColorScheme.dark(
                            primary: Colors.blue,
                            onPrimary: Colors.white,
                            surface: Colors.blue,
                            onSurface: Colors.black,
                          ),
                          dialogBackgroundColor: Colors.white,
                        ),
                        child: picker,
                      );
                    }).then((selectedDate) {
                  if (selectedDate != null) {
                    String myLocale =
                        Localizations.localeOf(context).toLanguageTag();
                    String date = DateFormat.yMd(myLocale)
                        .format(selectedDate)
                        .toString();
                    controllerEntrada.text = date;
                    notifyListeners();
                  }
                });
              },
            ),
          ],
        ),
        const SizedBox(height: 10),
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          Text(AppLocalizations.of(context).initialHour),
          SizedBox(width: MediaQuery.of(context).size.width * 0.10),
          SizedBox(
              width: MediaQuery.of(context).size.width * 0.30,
              child: TextField(
                controller: controllerHoraEntrada,
                enabled: false,
              )),
          IconButton(
            icon: const Icon(Icons.alarm),
            onPressed: () {
              showTimePicker(
                  initialTime: TimeOfDay(
                      hour: TimeOfDay.now().hour,
                      minute: TimeOfDay.now().minute),
                  context: context,
                  builder: (context, picker) {
                    return MediaQuery(
                        data: MediaQuery.of(context)
                            .copyWith(alwaysUse24HourFormat: true),
                        child: Theme(
                          data: ThemeData.dark().copyWith(
                            colorScheme: const ColorScheme.dark(
                              primary: Colors.deepPurple,
                              onPrimary: Colors.white,
                              surface: Colors.pink,
                              onSurface: Colors.yellow,
                            ),
                            dialogBackgroundColor: Colors.green[900],
                          ),
                          child: picker,
                        ));
                  }).then((selectedTime) {
                if (selectedTime != null) {
                  String time = selectedTime.hour.toString() +
                      ":" +
                      selectedTime.minute.toString();
                  controllerHoraEntrada.text = time;
                  notifyListeners();
                }
              });
            },
          )
        ]),
        const SizedBox(height: 10),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(AppLocalizations.of(context).finalDate),
            SizedBox(width: MediaQuery.of(context).size.width * 0.10),
            SizedBox(
                width: MediaQuery.of(context).size.width * 0.30,
                child: TextField(
                  controller: controllerSalida,
                  enabled: false,
                )),
            IconButton(
              icon: const Icon(Icons.calendar_today),
              onPressed: () {
                showDatePicker(
                    context: context,
                    initialDate: DateTime(2021, 10),
                    firstDate: DateTime(2021, 10),
                    lastDate: DateTime(2022, 12),
                    builder: (context, picker) {
                      return Theme(
                        data: ThemeData.dark().copyWith(
                          colorScheme: const ColorScheme.dark(
                            primary: Colors.blue,
                            onPrimary: Colors.white,
                            surface: Colors.blue,
                            onSurface: Colors.black,
                          ),
                          dialogBackgroundColor: Colors.white,
                        ),
                        child: picker,
                      );
                    }).then((selectedDate) {
                  if (selectedDate != null) {
                    String myLocale =
                        Localizations.localeOf(context).toLanguageTag();
                    String date = DateFormat.yMd(myLocale)
                        .format(selectedDate)
                        .toString();
                    controllerSalida.text = date;
                    notifyListeners();
                  }
                });
              },
            ),
          ],
        ),
        const SizedBox(height: 10),
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          Text(AppLocalizations.of(context).finalHour),
          SizedBox(width: MediaQuery.of(context).size.width * 0.10),
          SizedBox(
              width: MediaQuery.of(context).size.width * 0.30,
              child: TextField(
                controller: controllerHoraSalida,
                enabled: false,
              )),
          IconButton(
            icon: const Icon(Icons.alarm),
            onPressed: () {
              showTimePicker(
                  initialTime: TimeOfDay(
                      hour: TimeOfDay.now().hour,
                      minute: TimeOfDay.now().minute),
                  context: context,
                  builder: (context, picker) {
                    return MediaQuery(
                        data: MediaQuery.of(context)
                            .copyWith(alwaysUse24HourFormat: true),
                        child: Theme(
                          data: ThemeData.dark().copyWith(
                            colorScheme: const ColorScheme.dark(
                              primary: Colors.deepPurple,
                              onPrimary: Colors.white,
                              surface: Colors.pink,
                              onSurface: Colors.yellow,
                            ),
                            dialogBackgroundColor: Colors.green[900],
                          ),
                          child: picker,
                        ));
                  }).then((selectedTime) {
                if (selectedTime != null) {
                  String time = selectedTime.hour.toString() +
                      ":" +
                      selectedTime.minute.toString();
                  controllerHoraSalida.text = time;
                  notifyListeners();
                }
              });
            },
          )
        ])
      ]);
    }
  }

  String getFechaEntrada() {
    return controllerEntrada.text;
  }

  String getFechaSalida() {
    return controllerSalida.text;
  }

  String getHoraEntrada() {
    return controllerHoraEntrada.text;
  }

  String getHoraSalida() {
    return controllerHoraSalida.text;
  }
}

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider<dateChanger>(create: (context) => dateChanger()),
        ChangeNotifierProvider<dateChangerEvento>(
            create: (context) => dateChangerEvento()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'COVID App',
      theme: ThemeData(
          primarySwatch: Colors.blue,
          visualDensity: VisualDensity.adaptivePlatformDensity),
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      home: const MyHomePage(title: "Página Principal"),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String _qrcodeFile = '';
  String _data = '';
  ImagePicker _picker;
  ServerCalls database;
  File image;
  @override
  void initState() {
    super.initState();

    database = ServerCalls();
    _picker = ImagePicker();

    image = File("");
    dateformat.initializeDateFormatting('en', null);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: Text(AppLocalizations.of(context).paginaPrincipal),
          centerTitle: true),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Wrap(
              direction: Axis.vertical,
              spacing: MediaQuery.of(context).size.height * 0.25,
              children: [
                MaterialButton(
                    height: MediaQuery.of(context).size.height * 0.10,
                    minWidth: MediaQuery.of(context).size.width * 0.75,
                    onPressed: () async {
                      _qrcodeFile = await _imgFromGallery();
                      if (_qrcodeFile != null) {
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => AddQRManualPage(
                                    manual: false,
                                    name: _qrcodeFile.split(";")[0],
                                    surname: _qrcodeFile.split(";")[1],
                                    uuid: _qrcodeFile.split(";")[2])));
                      }
                    },
                    child: Text(AppLocalizations.of(context).addQr),
                    color: Theme.of(context).primaryColor,
                    textColor: Colors.white),
                MaterialButton(
                    height: MediaQuery.of(context).size.height * 0.10,
                    minWidth: MediaQuery.of(context).size.width * 0.75,
                    onPressed: () async {
                      var response;
                      try {
                        response = await database.getlistEvento();
                        Map<String, dynamic> responseJson =
                            json.decode(response.body);
                        Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => ListEvento(
                                value: false,
                                list: responseJson['access_log'])));
                      } on Exception catch (_) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                              content: Text(
                                  AppLocalizations.of(context).noServidor)),
                        );
                      }
                    },
                    child:
                        Text(AppLocalizations.of(context).gestionarListaEvento),
                    color: Theme.of(context).primaryColor,
                    textColor: Colors.white),
              ],
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
              context,
              MaterialPageRoute(
                  builder: (context) => AddQRManualPage(
                      manual: true, name: "", surname: "", uuid: "")));
        },
        child: const Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }

  _imgFromGallery() async {
    FilePickerResult result = await FilePicker.platform.pickFiles();

    if (result != null) {
      return await decode(
          "/storage/emulated/0/Download/" + result.files.single.name);
    } else {
      return null;
    }
  }

  Future decode(String file) async {
    String data = await QrCodeToolsPlugin.decodeFrom(file);
    return data;
  }

  _showPicker(context) async {
    showModalBottomSheet(
        context: context,
        builder: (BuildContext bc) {
          return SafeArea(
            child: Wrap(
              children: <Widget>[
                ListTile(
                    leading: const Icon(Icons.photo_library),
                    title: const Text('Galería'),
                    onTap: () async {
                      await _imgFromGallery();
                    }),
              ],
            ),
          );
        });
  }
}
