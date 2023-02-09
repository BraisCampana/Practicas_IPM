import 'dart:async';

import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class ServerCalls {
  ServerCalls();

  getUser(name, surname) async {
    var url = Uri.parse("http://10.0.2.2:8080/api/rest/user?name=" +
        name +
        "&surname=" +
        surname);
    var response = await http.get(
      url,
      headers: {
        "x-hasura-admin-secret": "myadminsecretkey",
      },
    );
    return response;
  }

  getUserByUuid(uuid) async {
    var url = Uri.parse("http://10.0.2.2:8080/api/rest/users/" + uuid);
    var response = await http.get(
      url,
      headers: {
        "x-hasura-admin-secret": "myadminsecretkey",
      },
    );
    var responseJson = json.decode(response.body);
    return responseJson["users"];
  }

  postAccess(infoUsers, index, temperature, timestamp, BuildContext context,
      fromQR) async {
    var url;
    http.Response response;
    String typeAnotacion = ""; //IN o OUT
    if (fromQR) {
      var listQR = await getUserByUuid(infoUsers[index]['uuid']);
      if (listQR.isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(AppLocalizations.of(context)!.userNotFound)),
        );
        return;
      }
    }
    try {
      response = await getlistEvento();
      List<dynamic> listEvento = json.decode(response.body)["access_log"];
      for (int i = 0; i < listEvento.length; i++) {
        //recorremos la lista por el final ya que está ordenada por fecha de forma descendiente
        if (listEvento[i]['user']['uuid'] == infoUsers[index]['uuid']) {
          typeAnotacion = listEvento[i]['type']; // IN o OUT
          break;
        }
      }
      if (typeAnotacion == "") {
        // si no se encontró al usuario en la lista anterior, es decir, nunca ha accedido o salido de la instalación
        //se le pone por defecto una entrada
        typeAnotacion = "IN";
      } else if (typeAnotacion == "IN") {
        typeAnotacion = "OUT";
      } else {
        typeAnotacion = "IN";
      }
      var submit = {
        "user_id": infoUsers[index]['uuid'],
        "facility_id": 130,
        "timestamp": timestamp,
        "type": typeAnotacion,
        "temperature": temperature
      };

      url = Uri.parse("http://10.0.2.2:8080/api/rest/access_log");
      try {
        response = await http.post(
          url,
          headers: {
            "x-hasura-admin-secret": "myadminsecretkey",
          },
          body: json.encode(submit),
        );
        if (typeAnotacion == "IN") {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(AppLocalizations.of(context)!.anotarE)),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(AppLocalizations.of(context)!.anotarS)),
          );
        }
      } on TimeoutException catch (_) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(AppLocalizations.of(context)!.noServidor)),
        );
      } on Exception catch (_) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(AppLocalizations.of(context)!.noServidor)),
        );
      }
    } on Exception catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(AppLocalizations.of(context)!.noServidor)),
      );
    }
  }

  getlistEvento() async {
    var url =
        Uri.parse("http://10.0.2.2:8080/api/rest/facility_access_log/130");
    var response = await http.get(
      url,
      headers: {
        "x-hasura-admin-secret": "myadminsecretkey",
      },
    );
    return response;
  }

  getListEventoRange(var data, Uri url, BuildContext context) async {
    http.Request request = http.Request("GET", url);
    request.body = json.encode(data);
    request.headers.addAll({"x-hasura-admin-secret": "myadminsecretkey"});
    http.Client client = http.Client();
    http.StreamedResponse streamedResponse;
    try {
      streamedResponse = await client.send(request);
      String response = await streamedResponse.stream.bytesToString();
      client.close();
      Map<String, dynamic> responseJson =
          json.decode(response) as Map<String, dynamic>;
      return responseJson;
    } on TimeoutException catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(AppLocalizations.of(context)!.noServidor)),
      );
    } on Exception catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(AppLocalizations.of(context)!.noServidor)),
      );
    }
  }

  getPeopleInside(List<dynamic> list) {
    var peopleIn, peopleOut;
    peopleIn = peopleOut = 0;
    for (int i = 0; i < list.length; i++) {
      if (list[i]['type'] == "IN") {
        peopleIn += 1;
      } else {
        peopleOut += 1;
      }
    }
    return peopleIn - peopleOut;
  }

  String getPeopleVisit(List<dynamic> list) {
    int count = 0;
    for (int i = 0; i < list.length; i++) {
      if (list[i]['type'] == "IN") {
        count++;
      }
    }
    return count.toString();
  }
}
