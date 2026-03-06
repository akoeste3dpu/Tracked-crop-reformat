import nuke

######Copy tracker animation curves to crop reformat
def cropFromTrack():
	# Get the selected node
	tracker_node = nuke.selectedNode()

	# Check if it's a Tracker node
	if tracker_node.Class() != 'Tracker4':
		nuke.message('Please select a Tracker node.')
		return

	# Create the Crop node
	crop_node = nuke.createNode('Crop')

	# Add custom user knob for the input format
	crop_node.addKnob(nuke.XY_Knob('input_format', 'input_format'))

	# Set expressions for the input format
	crop_node.knob('input_format').setExpression('width', 0)
	crop_node.knob('input_format').setExpression('height', 1)

	# Add custom user knobs for the tracker values
	translate_knob = nuke.XY_Knob('translate', 'translate')
	translate_knob.setVisible(False)
	crop_node.addKnob(translate_knob)

	center_knob = nuke.XY_Knob('center', 'center')
	center_knob.setVisible(False)
	crop_node.addKnob(center_knob)


	# Add a custom knob for the offset and size values
	crop_node.addKnob(nuke.XY_Knob('size', 'size'))
	crop_node.addKnob(nuke.XY_Knob('offset', 'Offset'))
	crop_node.addKnob(nuke.Int_Knob('scale'))

	# Set the default values
	crop_node['size'].setValue(256)
	crop_node['offset'].setValue(0.0)
	crop_node['scale'].setValue(1)

	# Copy the animation curves from the tracker to the crop node
	crop_node.knob('translate').fromScript(tracker_node.knob('translate').toScript())
	crop_node.knob('center').fromScript(tracker_node.knob('center').toScript())

	# Set expressions for the box knobs
	crop_node.knob('box').setExpression('int(center.x+translate.x-size.x+offset.x)', 0)
	crop_node.knob('box').setExpression('int(center.y+translate.y-size.y+offset.y)', 1)
	crop_node.knob('box').setExpression('int(center.x+translate.x+size.x+offset.x)', 2)
	crop_node.knob('box').setExpression('int(center.y+translate.y+size.y+offset.y)', 3)

	# Set the reformat knob to "1"
	crop_node.knob('reformat').setValue(1)

	# Create the Transform node
	transform_node = nuke.createNode('Transform')

	#Get the crop node's name
	crop_node_name = crop_node.name()

	# Set the expression for the Transform node's translate knobs
	transform_node['translate'].setExpression("{0}.box.x*{0}.scale".format(crop_node_name), 0)
	transform_node['translate'].setExpression("{0}.box.y*{0}.scale".format(crop_node_name), 1)

	# Set the filter of the Transform node to "impulse"
	transform_node['filter'].setValue('impulse')

	# Set the center of the Transform node to (0, 0)
	transform_node['center'].setValue([0, 0])

	# Create the final crop node
	final_crop_node = nuke.createNode('Crop')
	final_crop_node['reformat'].setValue(1)
	final_crop_node['intersect'].setValue(1)

	# Set the expression for the final crop node's box knobs
	final_crop_node['box'].setExpression("{0}.input_format.x*{0}.scale".format(crop_node_name), 2)
	final_crop_node['box'].setExpression("{0}.input_format.y*{0}.scale".format(crop_node_name), 3)


