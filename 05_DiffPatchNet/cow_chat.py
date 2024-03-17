import asyncio

import cowsay

clients = {}  # id -> Queue
logged_in = {}  # id -> Log/Not log
cows_match = {}  # id -> cow
used_cows = {}  # cow -> id


async def chat(reader, writer):
    # Login section
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    print(me)
    clients[me] = asyncio.Queue()
    logged_in[me] = False
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    # Separated values for

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive], return_when=asyncio.FIRST_COMPLETED
        )
        for q in done:
            if q is send:  # Sending section
                send = asyncio.create_task(reader.readline())

                message_list = q.result().decode().split()

                if len(message_list) == 0:
                    writer.write(
                        "Empty message is not allowed! Enter at least one character...".encode()
                    )
                    continue

                match message_list[0].strip():  # noqa: E999
                    case "who":  # list all used cows == cows_match.values()
                        loggedcowslist = "".join(
                            ["\n\t" + cow for cow in used_cows.keys()]
                        )
                        writer.write(f"Logged in cows are: {loggedcowslist}\n".encode())
                        await writer.drain()
                    case "cows":  # list all free cows
                        cowslist = "".join(
                            [
                                "\n\t" + cow
                                for cow in cowsay.list_cows()
                                if cow not in used_cows.keys()
                            ]
                        )
                        writer.write(
                            f"Available cows are:{cowslist}\n".encode()  # noqa: E501
                        )
                        await writer.drain()
                    case "quit":  # remove login and free used cow
                        logged_in[me] = False
                        del used_cows[cows_match[me]]
                        del cows_match[me]
                    case "login":
                        if not logged_in[me]:  # For users who are not logged yet
                            if len(message_list) < 2:  # Check if cow name is provided
                                writer.write(
                                    "Please, provide a cow name to log in\n".encode()
                                )
                                await writer.drain()
                            else:
                                cow_name = message_list[1].strip()
                                if (
                                    cow_name not in used_cows
                                    and cow_name in cowsay.list_cows()
                                ):  # Check cow name is correct
                                    cows_match[me] = cow_name
                                    used_cows[cow_name] = me
                                    logged_in[me] = True
                                    writer.write(
                                        f"You've logged in succesfully with cow name: {cow_name}\n".encode()
                                    )
                                elif cow_name in used_cows.keys():  # Used cow
                                    writer.write(
                                        f"Cow name {cow_name} is already exists! Pick a new one / call cows\n".encode()
                                    )
                                    await writer.drain()
                                else:  # Unexsistent cow
                                    writer.write(
                                        f"Cow name {cow_name} doesn't exist! Pick one, which exsists / call cows\n".encode()  # noqa: E501
                                    )
                                    await writer.drain()
                        else:  # Users, who've already logged
                            writer.write("You've already logged in\n".encode())
                            await writer.drain()
                    case "yield":
                        if logged_in[me]:
                            if len(message_list) < 2:  # Check if message is not empty
                                writer.write(
                                    "Please, enter at least one char\n".encode()
                                )
                                await writer.drain()
                            else:
                                message_to_all = " ".join(message_list[1:])
                                cow_message = cowsay.cowsay(
                                    message_to_all, cow=cows_match[me]
                                )
                                for logged_id in cows_match.keys():
                                    if logged_id != me and logged_in[logged_id]:
                                        out = clients[logged_id]
                                        await out.put(cow_message)
                        else:
                            writer.write(
                                "You cannot yield until you logged in\n".encode()
                            )
                            await writer.drain()
                    case "say":
                        if logged_in[me]:
                            if len(message_list) < 3:  # Check if message is not empty
                                writer.write(
                                    "Please, enter a target cow and at least one char\n".encode()
                                )
                                await writer.drain()
                            else:
                                target_cow = message_list[1].strip()
                                if target_cow in used_cows.keys():
                                    message_to_target = " ".join(message_list[2:])
                                    cow_message = cowsay.cowsay(
                                        message_to_target, cow=cows_match[me]
                                    )

                                    out = clients[used_cows[target_cow]]
                                    await out.put(cow_message)
                                else:
                                    writer.write(
                                        f"Target cow {target_cow} doesn't exsist. List available cows with who\n".encode()  # noqa: E501
                                    )
                                    await writer.drain()
                        else:
                            writer.write(
                                "You cannot say until you logged in\n".encode()
                            )
                            await writer.drain()
                    case _:
                        writer.write(
                            f"Unknown command {' '.join(message_list)}\n".encode()
                        )
                        await writer.drain()
            elif q is receive:  # Get msg
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    # Close connection section
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    del logged_in[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
