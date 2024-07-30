using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Reactive.Linq;
using System.Threading;
using System.Threading.Tasks;
using Bonsai;


/// <summary>
/// Represents an operator that starts a new system process with the specified file name and
/// command-line arguments.
/// </summary>
[DefaultProperty("FileName")]
[Description("Starts a new system process with the specified file name and command-line arguments.")]

public class CaptureProcess : Source<string>
{
    [Description("The name of the application or document to start.")]
    [FileNameFilter("Executable files|*.exe|All Files|*.*")]
    [Editor("Bonsai.Design.OpenFileNameEditor, Bonsai.Design", DesignTypes.UITypeEditor)]
    public string FileName { get; set; }

    [Editor(DesignTypes.MultilineStringEditor, DesignTypes.UITypeEditor)]
    [Description("The set of command-line arguments to use when starting the application.")]
    public string Arguments { get; set; }

    public IObservable<string> Generate<TSource>(IObservable<TSource> source)
    {
        return source.SelectMany(input => Generate());
    }

    public override IObservable<string> Generate()
    {
        return Observable.StartAsync(cancellationToken =>
        {
            return Task.Factory.StartNew(() =>
            {
                using (var exitSignal = new ManualResetEvent(false))
                using (var process = new Process())
                {
                    process.StartInfo.FileName = FileName;
                    process.StartInfo.Arguments = Arguments;
                    process.StartInfo.UseShellExecute = false;
                    process.StartInfo.RedirectStandardError = true;
                    process.StartInfo.RedirectStandardOutput = true;
                    process.Exited += (sender, e) => exitSignal.Set();
                    process.EnableRaisingEvents = true;
                    process.Start();
                    using (var cancellation = cancellationToken.Register(() => exitSignal.Set()))
                    {
                        exitSignal.WaitOne();
                        if (!process.HasExited){
                            throw new OperationCanceledException("Process did not exit in time");
                        }
                        var stdError = process.StandardError.ReadToEnd();
                        if (!string.IsNullOrEmpty(stdError))
                        {
                            throw new InvalidOperationException(stdError);
                        }
                        return process.StandardOutput.ReadToEnd();
;
                    }
                }
            },
            cancellationToken,
            TaskCreationOptions.LongRunning,
            TaskScheduler.Default);
        });
    }
}

