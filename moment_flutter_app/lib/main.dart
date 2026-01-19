import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const MoMentFlutterApp());
}

class MoMentFlutterApp extends StatelessWidget {
  const MoMentFlutterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MoMent',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
        cardTheme: const CardThemeData(elevation: 2),
      ),
      home: const HomeScreen(),
    );
  }
}
