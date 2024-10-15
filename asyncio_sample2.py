import asyncio


async def say_hello() -> None:
    """
    非同期タスク
    """
    print("start say_hello function")
    await asyncio.sleep(1)  # 1秒間待機（非同期）
    # time.sleep(1)
    print("end say_hello function")


async def run_command() -> None:
    """
    非同期で外部コマンドを実行
    """
    print("start run_command function")
    process = await asyncio.create_subprocess_exec(
        "sleep",
        "3",
        stdout=asyncio.subprocess.PIPE,  # 標準出力をキャプチャ
        stderr=asyncio.subprocess.PIPE,  # 標準エラー出力をキャプチャ
    )
    stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30.0)
    # stdout, stderr = await process.communicate()
    # print(f"[{process.returncode}]")
    if stdout:
        print(f"[stdout]\n{stdout.decode()}")
    if stderr:
        print(f"[stderr]\n{stderr.decode()}")
    print("end run_command function")


async def main() -> None:
    """
    メイン関数で非同期タスクを実行
    """
    await asyncio.gather(say_hello(), run_command(), say_hello())


if __name__ == "__main__":
    print("before run")
    asyncio.run(main())
    print("after run")
