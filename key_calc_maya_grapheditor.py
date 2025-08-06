import maya.cmds as cmds

def modify_key_values_ui():
    if cmds.window("modifyKeyWin", exists=True):
        cmds.deleteUI("modifyKeyWin")

    cmds.window("modifyKeyWin", title="キー値演算ツール", sizeable=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")

    cmds.text(label="演算対象：選択カーブ全キー値")
    value_field = cmds.floatField(value=1.0, precision=3)

    cmds.optionMenu("operationMenu", label="演算タイプ")
    cmds.menuItem(label="加算（+）")
    cmds.menuItem(label="減算（−）")
    cmds.menuItem(label="乗算（×）")
    cmds.menuItem(label="除算（÷）")

    cmds.button(label="適用", command=lambda *_: apply_operation_to_keys(
        cmds.optionMenu("operationMenu", q=True, value=True),
        cmds.floatField(value_field, q=True, value=True)
    ))

    cmds.showWindow()

def apply_operation_to_keys(operation, operand):
    selected_curves = cmds.keyframe(q=True, sl=True, name=True)
    if not selected_curves:
        cmds.warning("グラフエディタでカーブを選択してください。")
        return

    if operation == "除算（÷）" and operand == 0.0:
        cmds.warning("0で割ることはできません。")
        return

    for curve in set(selected_curves):
        key_count = cmds.keyframe(curve, q=True, keyframeCount=True)
        for i in range(key_count):
            time = cmds.keyframe(curve, index=(i,), q=True, timeChange=True)[0]
            value = cmds.keyframe(curve, index=(i,), q=True, valueChange=True)[0]

            if operation == "加算（+）":
                new_value = value + operand
            elif operation == "減算（−）":
                new_value = value - operand
            elif operation == "乗算（×）":
                new_value = value * operand
            elif operation == "除算（÷）":
                new_value = value / operand
            else:
                continue

            cmds.keyframe(curve, edit=True, time=(time,), valueChange=new_value)

    cmds.inViewMessage(
        amg=f"✅ <hl>{operation}</hl> を適用しました（値: {operand}）",
        pos="topCenter", fade=True
    )

modify_key_values_ui()