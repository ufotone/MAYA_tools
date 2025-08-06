import maya.cmds as cmds

class KeyTools:
    def __init__(self):
        self.window = "KeyToolsWindow"
        self.title = "Key Tools"
        self.size = (300, 400)
    def create(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)

        cmds.columnLayout(adjustableColumn=True)

        # 対象軸選択
        cmds.text(label="Select Axis:")
        self.axis_menu = cmds.optionMenu()
        cmds.menuItem(label="X")
        cmds.menuItem(label="Y")
        cmds.menuItem(label="Z")

        # タイムと値オフセット
        cmds.separator(style='in')
        cmds.text(label="Time and Value Offset:")
        self.time_offset_field = cmds.floatField(value=0.0)
        self.value_offset_field = cmds.floatField(value=0.0)
        cmds.button(label="Apply Offsets", command=self.apply_time_value_offsets)

        # 値を統一
        cmds.separator(style='in')
        cmds.text(label="Set Selected Keys to Same Value:")
        self.target_value_field = cmds.floatField(value=0.0)
        cmds.button(label="Same Value", command=self.set_same_value)

        # 値反転
        cmds.separator(style='in')
        cmds.text(label="Invert Selected Keys:")
        cmds.button(label="Invert Value", command=self.invert_values)

        # 平均値
        cmds.separator(style='in')
        cmds.text(label="Set Keys to Average:")
        cmds.button(label="Apply Average", command=self.apply_average)

        # 閾値以下のキー値を削除
        cmds.separator(style='in')
        cmds.text(label="Delete Keys Below Threshold:")
        self.threshold_field = cmds.floatField(value=0.0)
        cmds.button(label="Delete Keys", command=self.delete_keys_below_threshold)

        # Window表示
        cmds.showWindow(self.window)

    ####################################################################################
    def get_selected_axis(self):
        # 現在選択されている軸を取得
        return cmds.optionMenu(self.axis_menu, query=True, value=True)
    
    ####################################################################################
    def apply_time_value_offsets(self, *args):
        time_offset = cmds.floatField(self.time_offset_field, query=True, value=True)
        value_offset = cmds.floatField(self.value_offset_field, query=True, value=True)
        selected_objects = cmds.ls(selection=True)
        selected_axis = self.get_selected_axis()

        if not selected_objects:
            cmds.warning("No objects selected!")
            return

        for obj in selected_objects:
            attribute = f'translate{selected_axis}'
            selected_keys = cmds.keyframe(f"{obj}.{attribute}", query=True, selected=True, timeChange=True)
            if not selected_keys:
                cmds.warning(f"No keys selected for {obj}.{attribute}!")
                continue

            cmds.keyframe(f"{obj}.{attribute}", edit=True, relative=True,
                          time=(min(selected_keys), max(selected_keys)),
                          timeChange=time_offset, valueChange=value_offset)

    ####################################################################################
    def set_same_value(self, *args):
        target_value = cmds.floatField(self.target_value_field, query=True, value=True)
        selected_objects = cmds.ls(selection=True)
        selected_axis = self.get_selected_axis()

        if not selected_objects:
            cmds.warning("No objects selected!")
            return

        for obj in selected_objects:
            attribute = f'translate{selected_axis}'
            selected_keys = cmds.keyframe(f"{obj}.{attribute}", query=True, selected=True, timeChange=True)

            if not selected_keys:
                cmds.warning(f"No keys selected for {obj}.{attribute}!")
                continue

            cmds.keyframe(f"{obj}.{attribute}", edit=True, valueChange=target_value,
                          time=(min(selected_keys), max(selected_keys)))

    ####################################################################################
    def invert_values(self, *args):
        selected_objects = cmds.ls(selection=True)
        selected_axis = self.get_selected_axis()

        if not selected_objects:
            cmds.warning("No objects selected!")
            return

        for obj in selected_objects:
            attribute = f'translate{selected_axis}'
            selected_keys = cmds.keyframe(f"{obj}.{attribute}", query=True, selected=True, timeChange=True)
            values = cmds.keyframe(f"{obj}.{attribute}", query=True, selected=True, valueChange=True)

            if not selected_keys or not values:
                cmds.warning(f"No keys selected for {obj}.{attribute}!")
                continue

            inverted_values = [-v for v in values]
            for i, time in enumerate(selected_keys):
                cmds.setKeyframe(f"{obj}.{attribute}", time=time, value=inverted_values[i])

    ####################################################################################
    def apply_average(self, *args):
        selected_objects = cmds.ls(selection=True)
        selected_axis = self.get_selected_axis()

        if not selected_objects:
            cmds.warning("No objects selected!")
            return

        for obj in selected_objects:
            attribute = f'translate{selected_axis}'
            values = cmds.keyframe(f"{obj}.{attribute}", query=True, selected=True, valueChange=True)

            if not values:
                cmds.warning(f"No keys selected for {obj}.{attribute}!")
                continue

            average_value = sum(values) / len(values)
            selected_keys = cmds.keyframe(f"{obj}.{attribute}", query=True, selected=True, timeChange=True)
            for time in selected_keys:
                cmds.setKeyframe(f"{obj}.{attribute}", time=time, value=average_value)

    ####################################################################################
    def delete_keys_below_threshold(self, *args):
        threshold_value = cmds.floatField(self.threshold_field, query=True, value=True)
        selected_objects = cmds.ls(selection=True)
        selected_axis = self.get_selected_axis()

        if not selected_objects:
            cmds.warning("No objects selected!")
            return

        for obj in selected_objects:
            attribute = f'translate{selected_axis}'
            values = cmds.keyframe(f"{obj}.{attribute}", query=True, selected=True, valueChange=True)
            times = cmds.keyframe(f"{obj}.{attribute}", query=True, selected=True, timeChange=True)

            if not values or not times:
                cmds.warning(f"No keys selected for {obj}.{attribute}!")
                continue

            for i, value in enumerate(values):
                if value < threshold_value:
                    cmds.cutKey(f"{obj}.{attribute}", time=(times[i], times[i]))

####################################################################################
tool = KeyTools()
tool.create()