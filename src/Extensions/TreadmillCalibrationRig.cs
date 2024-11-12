//----------------------
// <auto-generated>
//     Generated using the NJsonSchema v10.9.0.0 (Newtonsoft.Json v13.0.0.0) (http://NJsonSchema.org)
// </auto-generated>
//----------------------


namespace AindBehaviorServices.TreadmillCalibrationRig
{
    #pragma warning disable // Disable all warnings

    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class BaseModel
    {
    
        public BaseModel()
        {
        }
    
        protected BaseModel(BaseModel other)
        {
        }
    
        public System.IObservable<BaseModel> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new BaseModel(this)));
        }
    
        public System.IObservable<BaseModel> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new BaseModel(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            return false;
        }
    
        public override string ToString()
        {
            System.Text.StringBuilder stringBuilder = new System.Text.StringBuilder();
            stringBuilder.Append(GetType().Name);
            stringBuilder.Append(" { ");
            if (PrintMembers(stringBuilder))
            {
                stringBuilder.Append(" ");
            }
            stringBuilder.Append("}");
            return stringBuilder.ToString();
        }
    }


    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class Treadmill
    {
    
        private string _deviceType = "treadmill";
    
        private BaseModel _additionalSettings;
    
        private TreadmillCalibration _calibration;
    
        private int _whoAmI = 1402;
    
        private string _serialNumber;
    
        private string _portName;
    
        public Treadmill()
        {
        }
    
        protected Treadmill(Treadmill other)
        {
            _deviceType = other._deviceType;
            _additionalSettings = other._additionalSettings;
            _calibration = other._calibration;
            _whoAmI = other._whoAmI;
            _serialNumber = other._serialNumber;
            _portName = other._portName;
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("device_type")]
        public string DeviceType
        {
            get
            {
                return _deviceType;
            }
            set
            {
                _deviceType = value;
            }
        }
    
        /// <summary>
        /// Additional settings
        /// </summary>
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("additional_settings")]
        [System.ComponentModel.DescriptionAttribute("Additional settings")]
        public BaseModel AdditionalSettings
        {
            get
            {
                return _additionalSettings;
            }
            set
            {
                _additionalSettings = value;
            }
        }
    
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("calibration")]
        public TreadmillCalibration Calibration
        {
            get
            {
                return _calibration;
            }
            set
            {
                _calibration = value;
            }
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("who_am_i")]
        public int WhoAmI
        {
            get
            {
                return _whoAmI;
            }
            set
            {
                _whoAmI = value;
            }
        }
    
        /// <summary>
        /// Device serial number
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("serial_number")]
        [System.ComponentModel.DescriptionAttribute("Device serial number")]
        public string SerialNumber
        {
            get
            {
                return _serialNumber;
            }
            set
            {
                _serialNumber = value;
            }
        }
    
        /// <summary>
        /// Device port name
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("port_name", Required=Newtonsoft.Json.Required.Always)]
        [System.ComponentModel.DescriptionAttribute("Device port name")]
        public string PortName
        {
            get
            {
                return _portName;
            }
            set
            {
                _portName = value;
            }
        }
    
        public System.IObservable<Treadmill> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new Treadmill(this)));
        }
    
        public System.IObservable<Treadmill> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new Treadmill(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            stringBuilder.Append("device_type = " + _deviceType + ", ");
            stringBuilder.Append("additional_settings = " + _additionalSettings + ", ");
            stringBuilder.Append("calibration = " + _calibration + ", ");
            stringBuilder.Append("who_am_i = " + _whoAmI + ", ");
            stringBuilder.Append("serial_number = " + _serialNumber + ", ");
            stringBuilder.Append("port_name = " + _portName);
            return true;
        }
    
        public override string ToString()
        {
            System.Text.StringBuilder stringBuilder = new System.Text.StringBuilder();
            stringBuilder.Append(GetType().Name);
            stringBuilder.Append(" { ");
            if (PrintMembers(stringBuilder))
            {
                stringBuilder.Append(" ");
            }
            stringBuilder.Append("}");
            return stringBuilder.ToString();
        }
    }


    /// <summary>
    /// Treadmill calibration class
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [System.ComponentModel.DescriptionAttribute("Treadmill calibration class")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class TreadmillCalibration
    {
    
        private string _deviceName = "Treadmill";
    
        private TreadmillCalibrationInput _input = new TreadmillCalibrationInput();
    
        private TreadmillCalibrationOutput _output = new TreadmillCalibrationOutput();
    
        private System.DateTimeOffset? _date;
    
        private string _description = "Calibration of the treadmill system";
    
        private string _notes;
    
        public TreadmillCalibration()
        {
        }
    
        protected TreadmillCalibration(TreadmillCalibration other)
        {
            _deviceName = other._deviceName;
            _input = other._input;
            _output = other._output;
            _date = other._date;
            _description = other._description;
            _notes = other._notes;
        }
    
        /// <summary>
        /// Must match a device name in rig/instrument
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("device_name")]
        [System.ComponentModel.DescriptionAttribute("Must match a device name in rig/instrument")]
        public string DeviceName
        {
            get
            {
                return _deviceName;
            }
            set
            {
                _deviceName = value;
            }
        }
    
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("input", Required=Newtonsoft.Json.Required.Always)]
        public TreadmillCalibrationInput Input
        {
            get
            {
                return _input;
            }
            set
            {
                _input = value;
            }
        }
    
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("output", Required=Newtonsoft.Json.Required.Always)]
        public TreadmillCalibrationOutput Output
        {
            get
            {
                return _output;
            }
            set
            {
                _output = value;
            }
        }
    
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("date")]
        public System.DateTimeOffset? Date
        {
            get
            {
                return _date;
            }
            set
            {
                _date = value;
            }
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("description")]
        public string Description
        {
            get
            {
                return _description;
            }
            set
            {
                _description = value;
            }
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("notes")]
        public string Notes
        {
            get
            {
                return _notes;
            }
            set
            {
                _notes = value;
            }
        }
    
        public System.IObservable<TreadmillCalibration> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new TreadmillCalibration(this)));
        }
    
        public System.IObservable<TreadmillCalibration> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new TreadmillCalibration(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            stringBuilder.Append("device_name = " + _deviceName + ", ");
            stringBuilder.Append("input = " + _input + ", ");
            stringBuilder.Append("output = " + _output + ", ");
            stringBuilder.Append("date = " + _date + ", ");
            stringBuilder.Append("description = " + _description + ", ");
            stringBuilder.Append("notes = " + _notes);
            return true;
        }
    
        public override string ToString()
        {
            System.Text.StringBuilder stringBuilder = new System.Text.StringBuilder();
            stringBuilder.Append(GetType().Name);
            stringBuilder.Append(" { ");
            if (PrintMembers(stringBuilder))
            {
                stringBuilder.Append(" ");
            }
            stringBuilder.Append("}");
            return stringBuilder.ToString();
        }
    }


    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class TreadmillCalibrationInput
    {
    
        public TreadmillCalibrationInput()
        {
        }
    
        protected TreadmillCalibrationInput(TreadmillCalibrationInput other)
        {
        }
    
        public System.IObservable<TreadmillCalibrationInput> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new TreadmillCalibrationInput(this)));
        }
    
        public System.IObservable<TreadmillCalibrationInput> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new TreadmillCalibrationInput(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            return false;
        }
    
        public override string ToString()
        {
            System.Text.StringBuilder stringBuilder = new System.Text.StringBuilder();
            stringBuilder.Append(GetType().Name);
            stringBuilder.Append(" { ");
            if (PrintMembers(stringBuilder))
            {
                stringBuilder.Append(" ");
            }
            stringBuilder.Append("}");
            return stringBuilder.ToString();
        }
    }


    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class TreadmillCalibrationOutput
    {
    
        private double _wheelDiameter = 15D;
    
        private int _pulsesPerRevolution = 28800;
    
        private bool _invertDirection = false;
    
        private System.Collections.Generic.List<System.Collections.Generic.List<double>> _brakeLookupCalibration = new System.Collections.Generic.List<System.Collections.Generic.List<double>>();
    
        public TreadmillCalibrationOutput()
        {
        }
    
        protected TreadmillCalibrationOutput(TreadmillCalibrationOutput other)
        {
            _wheelDiameter = other._wheelDiameter;
            _pulsesPerRevolution = other._pulsesPerRevolution;
            _invertDirection = other._invertDirection;
            _brakeLookupCalibration = other._brakeLookupCalibration;
        }
    
        /// <summary>
        /// Wheel diameter
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("wheel_diameter")]
        [System.ComponentModel.DescriptionAttribute("Wheel diameter")]
        public double WheelDiameter
        {
            get
            {
                return _wheelDiameter;
            }
            set
            {
                _wheelDiameter = value;
            }
        }
    
        /// <summary>
        /// Pulses per revolution
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("pulses_per_revolution")]
        [System.ComponentModel.DescriptionAttribute("Pulses per revolution")]
        public int PulsesPerRevolution
        {
            get
            {
                return _pulsesPerRevolution;
            }
            set
            {
                _pulsesPerRevolution = value;
            }
        }
    
        /// <summary>
        /// Invert direction
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("invert_direction")]
        [System.ComponentModel.DescriptionAttribute("Invert direction")]
        public bool InvertDirection
        {
            get
            {
                return _invertDirection;
            }
            set
            {
                _invertDirection = value;
            }
        }
    
        /// <summary>
        /// Brake lookup calibration. Each pair of values define (input [torque], output [brake set-point U16])
        /// </summary>
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("brake_lookup_calibration", Required=Newtonsoft.Json.Required.Always)]
        [System.ComponentModel.DescriptionAttribute("Brake lookup calibration. Each pair of values define (input [torque], output [bra" +
            "ke set-point U16])")]
        public System.Collections.Generic.List<System.Collections.Generic.List<double>> BrakeLookupCalibration
        {
            get
            {
                return _brakeLookupCalibration;
            }
            set
            {
                _brakeLookupCalibration = value;
            }
        }
    
        public System.IObservable<TreadmillCalibrationOutput> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new TreadmillCalibrationOutput(this)));
        }
    
        public System.IObservable<TreadmillCalibrationOutput> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new TreadmillCalibrationOutput(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            stringBuilder.Append("wheel_diameter = " + _wheelDiameter + ", ");
            stringBuilder.Append("pulses_per_revolution = " + _pulsesPerRevolution + ", ");
            stringBuilder.Append("invert_direction = " + _invertDirection + ", ");
            stringBuilder.Append("brake_lookup_calibration = " + _brakeLookupCalibration);
            return true;
        }
    
        public override string ToString()
        {
            System.Text.StringBuilder stringBuilder = new System.Text.StringBuilder();
            stringBuilder.Append(GetType().Name);
            stringBuilder.Append(" { ");
            if (PrintMembers(stringBuilder))
            {
                stringBuilder.Append(" ");
            }
            stringBuilder.Append("}");
            return stringBuilder.ToString();
        }
    }


    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class CalibrationRig
    {
    
        private string _aindBehaviorServicesPkgVersion = "0.8.7";
    
        private string _version = "0.0.0";
    
        private string _computerName;
    
        private string _rigName;
    
        private Treadmill _treadmill = new Treadmill();
    
        public CalibrationRig()
        {
        }
    
        protected CalibrationRig(CalibrationRig other)
        {
            _aindBehaviorServicesPkgVersion = other._aindBehaviorServicesPkgVersion;
            _version = other._version;
            _computerName = other._computerName;
            _rigName = other._rigName;
            _treadmill = other._treadmill;
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("aind_behavior_services_pkg_version")]
        public string AindBehaviorServicesPkgVersion
        {
            get
            {
                return _aindBehaviorServicesPkgVersion;
            }
            set
            {
                _aindBehaviorServicesPkgVersion = value;
            }
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("version")]
        public string Version
        {
            get
            {
                return _version;
            }
            set
            {
                _version = value;
            }
        }
    
        /// <summary>
        /// Computer name
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("computer_name")]
        [System.ComponentModel.DescriptionAttribute("Computer name")]
        public string ComputerName
        {
            get
            {
                return _computerName;
            }
            set
            {
                _computerName = value;
            }
        }
    
        /// <summary>
        /// Rig name
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("rig_name", Required=Newtonsoft.Json.Required.Always)]
        [System.ComponentModel.DescriptionAttribute("Rig name")]
        public string RigName
        {
            get
            {
                return _rigName;
            }
            set
            {
                _rigName = value;
            }
        }
    
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("treadmill", Required=Newtonsoft.Json.Required.Always)]
        public Treadmill Treadmill
        {
            get
            {
                return _treadmill;
            }
            set
            {
                _treadmill = value;
            }
        }
    
        public System.IObservable<CalibrationRig> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new CalibrationRig(this)));
        }
    
        public System.IObservable<CalibrationRig> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new CalibrationRig(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            stringBuilder.Append("aind_behavior_services_pkg_version = " + _aindBehaviorServicesPkgVersion + ", ");
            stringBuilder.Append("version = " + _version + ", ");
            stringBuilder.Append("computer_name = " + _computerName + ", ");
            stringBuilder.Append("rig_name = " + _rigName + ", ");
            stringBuilder.Append("treadmill = " + _treadmill);
            return true;
        }
    
        public override string ToString()
        {
            System.Text.StringBuilder stringBuilder = new System.Text.StringBuilder();
            stringBuilder.Append(GetType().Name);
            stringBuilder.Append(" { ");
            if (PrintMembers(stringBuilder))
            {
                stringBuilder.Append(" ");
            }
            stringBuilder.Append("}");
            return stringBuilder.ToString();
        }
    }


    /// <summary>
    /// Serializes a sequence of data model objects into JSON strings.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [System.ComponentModel.DescriptionAttribute("Serializes a sequence of data model objects into JSON strings.")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Transform)]
    public partial class SerializeToJson
    {
    
        private System.IObservable<string> Process<T>(System.IObservable<T> source)
        {
            return System.Reactive.Linq.Observable.Select(source, value => Newtonsoft.Json.JsonConvert.SerializeObject(value));
        }

        public System.IObservable<string> Process(System.IObservable<BaseModel> source)
        {
            return Process<BaseModel>(source);
        }

        public System.IObservable<string> Process(System.IObservable<Treadmill> source)
        {
            return Process<Treadmill>(source);
        }

        public System.IObservable<string> Process(System.IObservable<TreadmillCalibration> source)
        {
            return Process<TreadmillCalibration>(source);
        }

        public System.IObservable<string> Process(System.IObservable<TreadmillCalibrationInput> source)
        {
            return Process<TreadmillCalibrationInput>(source);
        }

        public System.IObservable<string> Process(System.IObservable<TreadmillCalibrationOutput> source)
        {
            return Process<TreadmillCalibrationOutput>(source);
        }

        public System.IObservable<string> Process(System.IObservable<CalibrationRig> source)
        {
            return Process<CalibrationRig>(source);
        }
    }


    /// <summary>
    /// Deserializes a sequence of JSON strings into data model objects.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [System.ComponentModel.DescriptionAttribute("Deserializes a sequence of JSON strings into data model objects.")]
    [System.ComponentModel.DefaultPropertyAttribute("Type")]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Transform)]
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<BaseModel>))]
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<Treadmill>))]
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<TreadmillCalibration>))]
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<TreadmillCalibrationInput>))]
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<TreadmillCalibrationOutput>))]
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<CalibrationRig>))]
    public partial class DeserializeFromJson : Bonsai.Expressions.SingleArgumentExpressionBuilder
    {
    
        public DeserializeFromJson()
        {
            Type = new Bonsai.Expressions.TypeMapping<CalibrationRig>();
        }

        public Bonsai.Expressions.TypeMapping Type { get; set; }

        public override System.Linq.Expressions.Expression Build(System.Collections.Generic.IEnumerable<System.Linq.Expressions.Expression> arguments)
        {
            var typeMapping = (Bonsai.Expressions.TypeMapping)Type;
            var returnType = typeMapping.GetType().GetGenericArguments()[0];
            return System.Linq.Expressions.Expression.Call(
                typeof(DeserializeFromJson),
                "Process",
                new System.Type[] { returnType },
                System.Linq.Enumerable.Single(arguments));
        }

        private static System.IObservable<T> Process<T>(System.IObservable<string> source)
        {
            return System.Reactive.Linq.Observable.Select(source, value => Newtonsoft.Json.JsonConvert.DeserializeObject<T>(value));
        }
    }
}