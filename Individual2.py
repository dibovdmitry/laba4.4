##!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import pathlib
import logging

"""
Выполнить индивидуальное задание 1 лабораторной работы 2.19, добавив возможность работы
с исключениями и логгирование.
"""


class Airplanes:
    def __init__(self, line):
        self.line = line

    def select_airplane(self, race):
        """
        Выбрать человека с заданной фамилией.
        """
        print(self.line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолёта"
            )
        )
        print(self.line)
        # Инициализировать счетчик.
        sel = input('Введите номер вашего самолёта: ')
        count = 0
        # Проверить людей из списка.
        for i, num in enumerate(race, 1):
            if sel == num['path']:
                count += 1
                print(
                    '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                        count,
                        num['path'],
                        num['model'],
                        ''.join((str(i) for i in num['number'])))),

        print(self.line)
        if count == 0:
            print('Никто не найден')
        print(self.line)

    def display(self, race):
        """
        Отобразить список людей.
        """
        print(self.line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолёта"
            )
        )
        print(self.line)
        for idx, airplane in enumerate(race, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    airplane['path'],
                    ''.join((str(i) for i in airplane['number'])),
                    airplane['model']
                )
            )
        print(self.line)

    def add_airplane(self, race, path, number, model):
        race.append(
            {
                'path': path,
                'number': number,
                'model': model,
            }
        )
        return race

    def save_airplane(self, file_name, race):
        with open(file_name, "w", encoding="utf-8") as file_out:
            json.dump(race, file_out, ensure_ascii=False, indent=4)
        logging.info(f"Данные сохранены в файл: {file_name}")

    def load_airplane(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f_in:
            return json.load(f_in)


def main(command_line=None):
    logging.basicConfig(
        filename='race.log',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    )

    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 20
    )
    fi = Airplanes(line)

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
    )
    parser = argparse.ArgumentParser("race")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    add = subparsers.add_parser(
        "add",
        parents=[file_parser]
    )
    add.add_argument(
        "-p",
        "--path",
        action="store",
        required=True,
    )
    add.add_argument(
        "-n",
        "--number",
        action="store"
    )
    add.add_argument(
        "-m",
        "--model",
        action="store",
        required=True,
    )
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
    )
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
    )
    args = parser.parse_args(command_line)

    is_dirty = False
    path = args.filename
    home = pathlib.Path.cwd() / path

    try:
        race = fi.load_airplane(home)
        logging.info("Файл найден")
    except FileNotFoundError:
        race = []
        logging.warning("Файл не найден, создается новый")

    if args.command == "add":
        race = fi.add_airplane(race, args.path, args.number, args.model)
        is_dirty = True
        logging.info("Добавлен рейс")
    elif args.command == 'display':
        fi.display(race)
        logging.info("Отображён список рейсов")
    elif args.command == "select":
        fi.select_airplane(race)
        logging.info("Выбран рейс с заданным номером")

    if is_dirty:
        fi.save_airplane(args.filename, race)


if __name__ == '__main__':
    main()
