import 'package:flutter/material.dart';
import 'server_calls.dart' as server;
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class MultipleUsers extends StatefulWidget {
  const MultipleUsers(
      {Key? key,
      required this.list,
      required this.temperature,
      required this.timestamp})
      : super(key: key);

  final List<dynamic> list;
  final String temperature;
  final String timestamp;

  @override
  State<MultipleUsers> createState() => _MultipleUsers();
}

class _MultipleUsers extends State<MultipleUsers> {
  final server.ServerCalls database = server.ServerCalls();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(AppLocalizations.of(context)!.selectUser),
          centerTitle: true,
          elevation: 0,
        ),
        body: ListView.builder(
            itemCount: widget.list.length,
            itemBuilder: (BuildContext context, int index) {
              return Card(
                  child: ListTile(
                      leading: const Icon(Icons.account_circle, size: 50.0),
                      title: Text(
                          widget.list[index]['name'] +
                              " " +
                              widget.list[index]['surname'],
                          style: const TextStyle(fontSize: 20.0)),
                      subtitle: Text(widget.list[index]['phone'] +
                          "\n" +
                          widget.list[index]['email']),
                      isThreeLine: true,
                      trailing: IconButton(
                          iconSize: 30.0,
                          icon: const Icon(Icons.info_outlined),
                          onPressed: () {
                            _buildPopupDialog(context, widget.list, index);
                          }),
                      onTap: () {
                        database.postAccess(
                            widget.list,
                            index,
                            widget.temperature,
                            widget.timestamp,
                            context,
                            false);
                      }));
            }));
  }
}

Future<dynamic> _buildPopupDialog(
    BuildContext context, List<dynamic> userList, int index) {
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
              Text("UUID: " + userList[index]['uuid']),
              Text(AppLocalizations.of(context)!.nombre +
                  ": " +
                  userList[index]['name']),
              Text(AppLocalizations.of(context)!.apellido +
                  ": " +
                  userList[index]['surname']),
              Text(AppLocalizations.of(context)!.nombreUser +
                  ": " +
                  userList[index]['username']),
              Text(AppLocalizations.of(context)!.telefono +
                  ": " +
                  userList[index]['phone']),
              Text(AppLocalizations.of(context)!.email +
                  ": " +
                  userList[index]['email']),
              Text(AppLocalizations.of(context)!.vacunado +
                  ": " +
                  userList[index]['is_vaccinated'].toString())
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
